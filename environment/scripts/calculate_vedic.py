
import sys
import re
import datetime
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib import aspects

# PATHS
CORE_DATA_PATH = "cases/001_Theodore/00_CORE_DATA/00_CORE_DATA.md"
OUTPUT_PATH = "cases/001_Theodore/00_CORE_DATA/05_VEDIC_SIDEREAL.md"

if len(sys.argv) > 1:
    OUTPUT_DIR = sys.argv[1]
    OUTPUT_PATH = f"{OUTPUT_DIR}/TEST_05_VEDIC_SIDEREAL.md"

# CONFIG: Set Ephemeris Path for High Precision / Stars
import os
import swisseph as swe
ephe_path = os.path.abspath("environment/data/sweph")
swe.set_ephe_path(ephe_path)


def parse_core_data():
    """Parses birth data from the CORE_DATA.md file."""
    with open(CORE_DATA_PATH, 'r') as f:
        content = f.read()

    # Extract Date
    date_match = re.search(r'\*\*Date:\*\* (.*)', content)
    date_str = date_match.group(1).strip() if date_match else "2007/04/24"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    for m, d in months.items():
        if m in date_str:
            parts = date_str.replace(',', '').split()
            date_str = f"{parts[2]}/{d}/{parts[1]}"
            break

    # Extract Time
    time_match = re.search(r'\*\*Time:\*\* (.*)', content)
    raw_time = time_match.group(1).split('(')[0].strip() if time_match else "04:15"
    if 'AM' in raw_time or 'PM' in raw_time:
        t_parts = raw_time.replace(':', ' ').split()
        h = int(t_parts[0])
        m = int(t_parts[1])
        ampm = t_parts[2]
        if ampm == 'PM' and h != 12: h += 12
        if ampm == 'AM' and h == 12: h = 0
        time_str = f"{h:02}:{m:02}"
    else:
        time_str = raw_time.strip()

    # Extract Timezone
    tz_match = re.search(r'\*\*Timezone:\*\* UTC([+-]\d+)', content)
    tz_offset = tz_match.group(1) if tz_match else "+03"
    if ':' not in tz_offset:
        tz_offset = f"{tz_offset}:00"
        if len(tz_offset) == 5:
             if tz_offset[1] not in ['0','1']:
                 tz_offset = tz_offset[0] + '0' + tz_offset[1:]

    # Extract Coordinates
    coord_match = re.search(r'\*\*Coordinates:\*\* (.*)', content)
    coord_raw = coord_match.group(1).strip() if coord_match else ""
    lat, lon = "47n01", "28e51" # Default
    
    decimal_match = re.findall(r'(\d+\.\d+)', coord_raw)
    if len(decimal_match) >= 2:
        lat_f = float(decimal_match[0])
        lon_f = float(decimal_match[1])
        
        # Convert to string format '46n59'
        d_lat = int(lat_f)
        m_lat = int((lat_f - d_lat) * 60)
        suffix_lat = 'n' if lat_f >= 0 else 's'
        lat = f"{d_lat}{suffix_lat}{m_lat:02d}"
        
        d_lon = int(lon_f)
        m_lon = int((lon_f - d_lon) * 60)
        suffix_lon = 'e' if lon_f >= 0 else 'w'
        lon = f"{d_lon}{suffix_lon}{m_lon:02d}"

    return date_str, time_str, tz_offset, lat, lon

def generate_markdown(chart, ayanamsa):
    md = "# 04 VEDIC CHART (SIDEREAL LAHIRI)\n\n"
    md += f"**Calculated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += f"**Mode:** Sidereal (Lahiri Ayanamsa: {ayanamsa:.4f}°)\n"
    md += "---\n\n"
    
    md += "## 1. PLANETARY POSITIONS (LAHIRI)\n"
    md += "| Planet | Sign | Degree | House | Nakshatra |\n"
    md += "|:---|:---|:---|:---|:---|\n"
    
    objects = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
        const.NORTH_NODE, const.SOUTH_NODE
    ]
    
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    for obj in objects:
        p = chart.get(obj)
        retro = "R" if p.isRetrograde() else ""
        
        # Sidereal Calc
        sid_lon = (p.lon - ayanamsa) % 360
        
        s_idx = int(sid_lon // 30)
        sign_name = signs[s_idx]
        d = int(sid_lon) % 30
        m = int((sid_lon - int(sid_lon)) * 60)
        
        # House (Using simple bounds check against Sidereal House Cusps? Or just keep Placidus houses shifted?
        # Vedic usually uses Rasi chart (Whole Sign).
        # We will assume Whole Sign relative to Sidereal Ascendant for "House" column here effectively.
        # But for now, let's just output the positions.
        h_num = "--" # Placeholder or expensive calc
        
        nakshatra = "Unknown" 
        md += f"| **{obj}** | {sign_name} | {d:02d}°{m:02d}' | {h_num} | {retro} |\n"

    md += "\n## 2. HOUSE CUSP (SIDEREAL PLACIDUS)\n"
    md += "| House | Sign | Degree |\n"
    md += "|:---|:---|:---|\n"
    
    for h in chart.houses:
        sid_lon = (h.lon - ayanamsa) % 360
        s_idx = int(sid_lon // 30)
        sign_name = signs[s_idx]
        d = int(sid_lon) % 30
        m = int((sid_lon - int(sid_lon)) * 60)
        md += f"| **{h.id}** | {sign_name} | {d:02d}°{m:02d}' |\n"
        
    return md

def main():
    date_str, time_str, tz_offset, lat, lon = parse_core_data()
    date = Datetime(date_str, time_str, tz_offset)
    pos = GeoPos(lat, lon)
    
    # Calculate Tropical Chart first
    chart = Chart(date, pos, hsys=const.HOUSES_PLACIDUS, IDs=const.LIST_OBJECTS)
    
    # Calculate Lahiri Ayanamsa using swisseph directly
    import swisseph as swe
    # flatlib date.jd is Julian Day (UT calculation depends on flatlib implementation, usually it's ET or UT)
    # flatlib.datetime.Datetime stores jd (Julian Day)
    
    # Enable Lahiri
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    # get_ayanamsa_ut requires JD in UT. flatlib date.jd is usually UT if timezone handled correctly.
    ayanamsa = swe.get_ayanamsa_ut(date.jd)
    
    print(f"Lahiri Ayanamsa: {ayanamsa}")
    
    # Generate Markdown with manual Sidereal conversion
    md_content = generate_markdown(chart, ayanamsa)
    
    with open(OUTPUT_PATH, 'w') as f:
        f.write(md_content)
    print(f"Successfully updated {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
