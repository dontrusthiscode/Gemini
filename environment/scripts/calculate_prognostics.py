
import sys
import re
import datetime
import math

try:
    import flatlib
    import swisseph as swe
    from flatlib.datetime import Datetime
    from flatlib.geopos import GeoPos
    from flatlib.chart import Chart
    from flatlib import const
    from flatlib import aspects
except ImportError:
    print("Error: 'flatlib' or 'pyswisseph' not found.")
    sys.exit(1)

# CONFIG: Set Ephemeris Path for High Precision / Stars
import os
ephe_path = os.path.abspath("environment/data/sweph")
swe.set_ephe_path(ephe_path)

# PATHS
CORE_DATA_PATH = "cases/001_Theodore/00_CORE_DATA/00_CORE_DATA.md"

# Output Logic
if len(sys.argv) > 1:
    OUTPUT_DIR = sys.argv[1]
else:
    # Default to current session or fallback
    # If session 001 is gone, use a temp folder or harmonization folder
    OUTPUT_DIR = "scratches/sessions/001_Refine_Coordinates"
    if not os.path.exists(OUTPUT_DIR):
        OUTPUT_DIR = "scratches/harmonization_build"
        os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_SA = f"{OUTPUT_DIR}/TEST_02_SOLAR_ARC.md"
OUTPUT_PROG = f"{OUTPUT_DIR}/TEST_04_PROGRESSIONS.md"
OUTPUT_SR = f"{OUTPUT_DIR}/TEST_08_SOLAR_RETURN.md"

# ---------------------------------------------------------
# 1. PARSER (Reused from calculate_natal.py logic)
# ---------------------------------------------------------
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
             if tz_offset[1] != '0' and tz_offset[1] != '1':
                 tz_offset = tz_offset[0] + '0' + tz_offset[1:]

    # Extract Coordinates
    coord_match = re.search(r'\*\*Coordinates:\*\* (.*)', content)
    coord_raw = coord_match.group(1).strip() if coord_match else ""
    lat, lon = "47n01", "28e51" # Fallback
    decimal_match = re.findall(r'(\d+\.\d+)', coord_raw)
    if len(decimal_match) >= 2:
        lat_f = float(decimal_match[0])
        lon_f = float(decimal_match[1])
        d_lat = int(lat_f); m_lat = int((lat_f - d_lat) * 60); suffix_lat = 'n' if lat_f >= 0 else 's'
        lat = f"{d_lat}{suffix_lat}{m_lat:02d}"
        d_lon = int(lon_f); m_lon = int((lon_f - d_lon) * 60); suffix_lon = 'e' if lon_f >= 0 else 'w'
        lon = f"{d_lon}{suffix_lon}{m_lon:02d}"

    return date_str, time_str, tz_offset, lat, lon

# ---------------------------------------------------------
# 2. CALCULATION ENGINES
# ---------------------------------------------------------

def get_orb_str(orb):
    d = int(orb)
    m = int((orb - d) * 60)
    return f"{d}°{m:02d}'"

def format_pos(p):
    d = int(p.lon) % 30
    m = int((p.lon - int(p.lon)) * 60)
    return f"{p.sign} {d:02d}°{m:02d}'"

def calculate_solar_arc(natal_chart, natal_date_utc, target_year=2026, target_month=10, target_day=23):
    """
    Solar Arc: Sun's motion in days = Years of life.
    We add that arc to EVERYTHING.
    """
    # natal_date_utc.date.toList() returns ['+', 2007, 4, 24]
    birth_year = natal_date_utc.date.toList()[1]
    years = target_year - birth_year
    # Simply: Age in days. 
    # Accurate Solar Arc: Position of Secondary Progressed Sun - Natal Sun = ARC.
    # 1. Calculate Natal Sun
    n_sun = natal_chart.get(const.SUN)
    
    # 2. Calculate Progressed Sun (Day for Year)
    # Target Age
    target_date = datetime.datetime(target_year, target_month, target_day)
    birth_dt = datetime.datetime.strptime(f"{natal_date_utc.date.toString()} {natal_date_utc.time.toString()}", "%Y/%m/%d %H:%M:%S")
    days_alive = (target_date - birth_dt).days
    
    # Progression: Add 'days_alive / 365.25' days to birth DATE? No.
    # Secondary Progression: 1 day after birth = 1 year of life.
    # Age = 18.5 years.
    # Add 18.5 days to birth time.
    age_years = (target_date - birth_dt).days / 365.242199
    
    prog_delta = datetime.timedelta(days=age_years)
    prog_time_dt = birth_dt + prog_delta
    
    # Create Progressed Chart to get Sun
    # Note: flatlib Datetime requires string format
    p_date_str = prog_time_dt.strftime('%Y/%m/%d')
    p_time_str = prog_time_dt.strftime('%H:%M')
    
    # We must use same UT offset for progression calculation logic usually, 
    # but strictly it's adding days to the Ephemeris time.
    # Let's assume input chart is UTC.
    prog_dt_flat = Datetime(p_date_str, p_time_str, '+00:00')
    prog_chart = Chart(prog_dt_flat, natal_chart.pos, IDs=const.LIST_OBJECTS)
    
    p_sun = prog_chart.get(const.SUN)
    
    # Arc = P_Sun - N_Sun
    arc = p_sun.lon - n_sun.lon
    if arc < 0: arc += 360
    
    # Generate Output
    md = "# 02 SOLAR ARC DIRECTIONS\n\n"
    md += f"**Target Date:** {target_year}-{target_month:02d}-{target_day:02d}\n"
    md += f"**Solar Arc:** {arc:.4f}°\n"
    md += "---\n\n"
    md += "| Planet | Natal | Solar Arc | Aspect to Natal |\n"
    md += "|:---|:---|:---|:---|\n"
    
    objects = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
               const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
               const.NORTH_NODE, const.MC, const.ASC]
               
    for obj in objects:
        n_p = natal_chart.get(obj)
        # Apply Arc
        sa_lon = (n_p.lon + arc) % 360
        
        # Determine Sign/Deg
        sign_idx = int(sa_lon / 30)
        sign = const.LIST_SIGNS[sign_idx]
        deg = sa_lon % 30
        d_int = int(deg)
        m_int = int((deg - d_int) * 60)
        sa_pos_str = f"{sign} {d_int:02d}°{m_int:02d}'"
        
        # Check Aspects to Natal
        aspect_str = ""
        # Dummy object for SA position
        class Dummy:
            def __init__(self, l): self.lon = l
        
        sa_obj = Dummy(sa_lon)
        
        # Check against all natal objects
        hits = []
        for n_target in objects:
            n_t_p = natal_chart.get(n_target)
            
            # Simple Aspect Math
            diff = abs(sa_obj.lon - n_t_p.lon)
            if diff > 180: diff = 360 - diff
            
            # Conjunction, Square, Opposition only (Hard Aspects usually for SA)
            found = None
            orb = 0
            if diff < 1.0: found="Conj"; orb=diff
            elif abs(diff-90) < 1.0: found="Sqr"; orb=abs(diff-90)
            elif abs(diff-180) < 1.0: found="Opp"; orb=abs(diff-180)
            
            if found:
                hits.append(f"{found} {n_target} ({get_orb_str(orb)})")
                
        aspect_str = ", ".join(hits)
        
        md += f"| **{obj}** | {format_pos(n_p)} | **{sa_pos_str}** | {aspect_str} |\n"
        
    return md

def calculate_progressions(natal_chart, natal_date_utc, target_year=2026):
    """
    Secondary Progressions: A day for a year.
    Ref Age: 19 (in 2026).
    """
    # Logic similar to SA for time calculation
    # Target Date: April 24, 2026 (Birthday)
    target_date = datetime.datetime(target_year, 4, 24)
    birth_dt = datetime.datetime.strptime(f"{natal_date_utc.date.toString()} {natal_date_utc.time.toString()}", "%Y/%m/%d %H:%M:%S")
    
    # Exact days elapsed (Real Time)
    days_alive_real = (target_date - birth_dt).days
    age_years = days_alive_real / 365.242199
    
    # Secondary Progression: 1 Day = 1 Year
    prog_delta = datetime.timedelta(days=age_years)
    prog_time_dt = birth_dt + prog_delta # This is the "Progressed Date" in 2007
    
    p_date_str = prog_time_dt.strftime('%Y/%m/%d')
    p_time_str = prog_time_dt.strftime('%H:%M')
    
    prog_dt_flat = Datetime(p_date_str, p_time_str, '+00:00')
    prog_chart = Chart(prog_dt_flat, natal_chart.pos, IDs=const.LIST_OBJECTS)
    
    md = "# 04 SECONDARY PROGRESSIONS\n\n"
    md += f"**Target Year:** {target_year}\n"
    md += f"**Progressed Date:** {p_date_str} {p_time_str} UTC\n"
    md += "---\n\n"
    md += "| Planet | Progressed Pos | Motion | Aspect to Natal |\n"
    md += "|:---|:---|:---|:---|\n"
    
    objects = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
               const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
               const.NORTH_NODE, const.MC, const.ASC]
               
    for obj in objects:
        p_p = prog_chart.get(obj)
        retro = "R" if hasattr(p_p, 'isRetrograde') and p_p.isRetrograde() else ""
        
        # Check Aspects to Natal
        hits = []
        for n_target in objects:
            n_t_p = natal_chart.get(n_target)
            try:
                aspect = aspects.getAspect(p_p, n_t_p, const.MAJOR_ASPECTS)
            except: continue
            
            if aspect.exists() and aspect.orb < 1.0:
                hits.append(f"{aspect.type} {n_target} ({get_orb_str(aspect.orb)})")
        
        aspect_str = ", ".join(hits)
        md += f"| **{obj}** | {format_pos(p_p)} {retro} | {retro} | {aspect_str} |\n"
        
    return md

def calculate_solar_return(natal_chart, natal_date_utc, target_year=2026):
    """
    Solar Return: Sun returns to exact natal longitude.
    """
    n_sun = natal_chart.get(const.SUN)
    n_sun_lon = n_sun.lon
    
    # Search around birthday in target year
    # Start search 2 days before birthday
    search_start = datetime.datetime(target_year, 4, 22)
    
    # Iterative search (Binary Search or Sweph internal?)
    # Generating a series of times is inefficient.
    # flatlib doesn't have a "solar return" solver.
    # We will estimate or skip strict calculation if too complex?
    # NO. We are The Investigator. We calculate.
    
    # Using pyswisseph for precision if possible.
    # swe.sol_cross(natal_sun_lon, jd_start, ...)?
    # swe.solcross is not standard.
    
    # Simple binary search in python:
    # Find time t where Sun(t) == n_sun_lon
    
    low = search_start
    high = search_start + datetime.timedelta(days=4)
    
    final_dt = None
    
    for _ in range(20): # 20 iterations ~ seconds precision
        mid = low + (high - low) / 2
        
        # Get Sun Pos at mid
        d_str = mid.strftime('%Y/%m/%d')
        t_str = mid.strftime('%H:%M:%S')
        dt_flat = Datetime(d_str, t_str, '+00:00')
        c = Chart(dt_flat, natal_chart.pos, IDs=[const.SUN])
        s_lon = c.get(const.SUN).lon
        
        diff = s_lon - n_sun_lon
        # Handle wrap around 360/0
        if diff > 180: diff -= 360
        if diff < -180: diff += 360
        
        if diff > 0:
            high = mid
        else:
            low = mid
            
    final_dt = low
    
    # Generate Chart for this time
    d_str = final_dt.strftime('%Y/%m/%d')
    t_str = final_dt.strftime('%H:%M:%S')
    sr_date = Datetime(d_str, t_str, '+00:00')
    sr_chart = Chart(sr_date, natal_chart.pos, IDs=const.LIST_OBJECTS)
    
    md = "# 08 SOLAR RETURN\n\n"
    md += f"**Target Year:** {target_year}\n"
    md += f"**Return Date:** {d_str} {t_str} UTC\n"
    md += "---\n\n"
    md += "| Planet | Sign | Degree | House | Retro |\n"
    md += "|:---|:---|:---|:---|:---|\n"
    
    objects = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
               const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
               const.NORTH_NODE, const.MC, const.ASC]
               
    for obj in objects:
        p = sr_chart.get(obj)
        retro = "R" if hasattr(p, 'isRetrograde') and p.isRetrograde() else ""
        
        # Houses
        h_num = -1
        for h in sr_chart.houses:
            if h.inHouse(p.lon):
                h_num = h.id
                break
                
        md += f"| **{obj}** | {p.sign} | {get_orb_str(p.lon % 30)} | {h_num} | {retro} |\n"
        
    return md

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    print("Parsing Core Data...")
    date_str, time_str, tz_offset, lat, lon = parse_core_data()
    print(f"Birth: {date_str} {time_str} {tz_offset} | Loc: {lat}, {lon}")
    
    # Natal Chart
    date = Datetime(date_str, time_str, tz_offset)
    pos = GeoPos(lat, lon)
    natal = Chart(date, pos, IDs=const.LIST_OBJECTS)
    
    print("Calculating Solar Arc...")
    md_sa = calculate_solar_arc(natal, date)
    with open(OUTPUT_SA, 'w') as f: f.write(md_sa)
    
    print("Calculating Progressions...")
    md_prog = calculate_progressions(natal, date)
    with open(OUTPUT_PROG, 'w') as f: f.write(md_prog)
    
    print("Calculating Solar Return...")
    md_sr = calculate_solar_return(natal, date)
    with open(OUTPUT_SR, 'w') as f: f.write(md_sr)
    
    print("Done. Check 'scratches/sessions/001_Refine_Coordinates/'")

if __name__ == "__main__":
    main()
