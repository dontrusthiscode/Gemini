
import sys
import re
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib import aspects

# PATHS
CORE_DATA_PATH = "cases/001_Theodore/00_CORE_DATA/00_CORE_DATA.md"
OUTPUT_PATH = "cases/001_Theodore/00_CORE_DATA/01_NATAL_CHART.md"

# CONFIG: Set Ephemeris Path for High Precision / Stars
import os
import swisseph as swe
ephe_path = os.path.abspath("environment/data/sweph")
swe.set_ephe_path(ephe_path)

if len(sys.argv) > 1:
    OUTPUT_DIR = sys.argv[1]
    OUTPUT_PATH = f"{OUTPUT_DIR}/TEST_01_NATAL_CHART.md"


def parse_core_data():
    """Parses birth data from the CORE_DATA.md file."""
    with open(CORE_DATA_PATH, 'r') as f:
        content = f.read()

    # Extract Date: "April 24, 2007"
    date_match = re.search(r'\*\*Date:\*\* (.*)', content)
    date_str = date_match.group(1).strip() if date_match else "2007/04/24"
    # Convert "April 24, 2007" to "2007/04/24" for flatlib
    # Simple map for months
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    for m, d in months.items():
        if m in date_str:
            parts = date_str.replace(',', '').split() # ['April', '24', '2007']
            # date_str becomes 2007/04/24
            date_str = f"{parts[2]}/{d}/{parts[1]}"
            break

    # Extract Time: "04:15 AM" -> "04:15" (Flatlib expects 24h usually, but we need to handle AM/PM)
    time_match = re.search(r'\*\*Time:\*\* (.*)', content)
    raw_time = time_match.group(1).split('(')[0].strip() if time_match else "04:15"
    # Convert to 24h format
    if 'AM' in raw_time or 'PM' in raw_time:
        t_parts = raw_time.replace(':', ' ').split()
        h = int(t_parts[0])
        m = int(t_parts[1])
        ampm = t_parts[2]
        if ampm == 'PM' and h != 12:
            h += 12
        if ampm == 'AM' and h == 12:
            h = 0
        time_str = f"{h:02}:{m:02}"
    else:
        time_str = raw_time.strip()

    # Extract Timezone: "UTC+3"
    tz_match = re.search(r'\*\*Timezone:\*\* UTC([+-]\d+)', content)
    tz_offset = tz_match.group(1) if tz_match else "+03"
    # Flatlib expects UT offset in format "+03:00"
    if ':' not in tz_offset:
        tz_offset = f"{tz_offset}:00"
        if len(tz_offset) == 5: # +3:00 -> +03:00
             if tz_offset[1] != '0' and tz_offset[1] != '1': # Check if single digit hour
                 tz_offset = tz_offset[0] + '0' + tz_offset[1:]

    # Extract Coordinates
    # Looking for: "**Coordinates:** [PENDING PRECISE UPDATE] (Current: 47°01′N 28°51′E)"
    # OR format: 47n01, 28e51
    # We will try to parse decimal first if user updated it, else fallback to the string
    coord_match = re.search(r'\*\*Coordinates:\*\* (.*)', content)
    coord_raw = coord_match.group(1).strip() if coord_match else ""
    
    lat, lon = "47n01", "28e51" # Default fallback
    
    # Try to find decimal coordinates [47.123, 28.123]
    decimal_match = re.findall(r'(\d+\.\d+)', coord_raw)
    if len(decimal_match) >= 2:
        lat_f = float(decimal_match[0])
        lon_f = float(decimal_match[1])
        
        # Convert to string format '46n59'
        # Latitude
        d_lat = int(lat_f)
        m_lat = int((lat_f - d_lat) * 60)
        suffix_lat = 'n' if lat_f >= 0 else 's'
        lat = f"{d_lat}{suffix_lat}{m_lat:02d}"
        
        # Longitude
        d_lon = int(lon_f)
        m_lon = int((lon_f - d_lon) * 60)
        suffix_lon = 'e' if lon_f >= 0 else 'w'
        lon = f"{d_lon}{suffix_lon}{m_lon:02d}"
        
        print(f"Decimal Coordinates Detected. Converted to: {lat}, {lon}")

    print(f"Parsed: {date_str} {time_str} {tz_offset}")
    return date_str, time_str, tz_offset, lat, lon

def generate_markdown(chart):
    """Generates the markdown content for 01_NATAL_CHART.md"""
    
    md = "# 01 NATAL CHART (PLACIDUS)\n\n"
    import datetime
    md += f"**Calculated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += "---\n\n"
    
    md += "## 1. PLANETARY POSITIONS\n"
    md += "| Planet | Sign | Degree | House | Retro |\n"
    md += "|:---|:---|:---|:---|:---|\n"
    
    objects = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
        const.NORTH_NODE, const.SOUTH_NODE, const.CHIRON
    ]
    
    for obj in objects:
        p = chart.get(obj)
        retro = "R" if p.isRetrograde() else ""
        # Format degree: 25.123 -> 25°07'
        d = int(p.lon) % 30
        m = int((p.lon - int(p.lon)) * 60)
        
        # House placement (simple approximation if not using full house object)
        # Using chart.houses.getHouse(p.lon) logic if available?
        # Flatlib chart object has houses list.
        h_num = -1
        for h in chart.houses:
            if h.inHouse(p.lon):
                h_num = h.id
                break
                
        md += f"| **{obj}** | {p.sign} | {d:02d}°{m:02d}' | {h_num} | {retro} |\n"

    md += "\n## 2. HOUSE CUSPS (PLACIDUS)\n"
    md += "| House | Sign | Degree |\n"
    md += "|:---|:---|:---|\n"
    
    for h in chart.houses:
        d = int(h.lon) % 30
        m = int((h.lon - int(h.lon)) * 60)
        md += f"| **{h.id}** | {h.sign} | {d:02d}°{m:02d}' |\n"
        
    md += "\n## 3. NUCLEAR EVENTS (< 1°)\n"
    md += "| Planet A | Aspect | Planet B | Orb |\n"
    md += "|:---|:---|:---|:---|\n"

    # Calculate tight aspects
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i >= j: continue # Avoid duplicates and self-aspects
            
            p1 = chart.get(obj1)
            p2 = chart.get(obj2)
            
            # Get Aspect
            try:
                aspect = aspects.getAspect(p1, p2, const.MAJOR_ASPECTS)
            except:
                continue
                
            if aspect.exists():
                orb = aspect.orb
                if orb < 1.0: # NUCLEAR FILTER
                    d_orb = int(orb)
                    m_orb = int((orb - d_orb) * 60)
                    orb_str = f"{d_orb}°{m_orb:02d}'"
                    orb_display = f"**{orb_str}**" if orb < 0.2 else orb_str
                    md += f"| **{obj1}** | {aspect.type} | **{obj2}** | {orb_display} |\n"
    
    return md

def main():
    date_str, time_str, tz_offset, lat, lon = parse_core_data()
    
    # Create Date Object
    date = Datetime(date_str, time_str, tz_offset)
    pos = GeoPos(lat, lon)
    
    chart = Chart(date, pos, hsys=const.HOUSES_PLACIDUS, IDs=const.LIST_OBJECTS)
    
    md_content = generate_markdown(chart)
    
    with open(OUTPUT_PATH, 'w') as f:
        f.write(md_content)
        
    print(f"Successfully updated {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
