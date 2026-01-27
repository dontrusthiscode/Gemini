
import sys
import re
import datetime
import math

try:
    import swisseph as swe
except ImportError:
    print("Error: 'pyswisseph' not found.")
    sys.exit(1)

# PATHS
CORE_DATA_PATH = "cases/001_Theodore/00_CORE_DATA/00_CORE_DATA.md"

# Output Logic
if len(sys.argv) > 1:
    OUTPUT_DIR = sys.argv[1]
else:
    OUTPUT_DIR = "scratches/sessions/001_Refine_Coordinates"
    if not os.path.exists(OUTPUT_DIR):
        OUTPUT_DIR = "scratches/harmonization_build"
        os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_DETAILS = f"{OUTPUT_DIR}/TEST_06_VEDIC_DETAILS.md"
OUTPUT_DASHA = f"{OUTPUT_DIR}/TEST_09_DASHA_TIMELINE.md"
OUTPUT_VARGA = f"{OUTPUT_DIR}/TEST_10_DIVISIONALS.md"

# ---------------------------------------------------------
# 1. PARSER (Redundant but safe)
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
    lat_f, lon_f = 46.98, 28.87
    
    decimal_match = re.findall(r'(\d+\.\d+)', coord_raw)
    if len(decimal_match) >= 2:
        lat_f = float(decimal_match[0])
        lon_f = float(decimal_match[1])

    return date_str, time_str, tz_offset, lat_f, lon_f

# ---------------------------------------------------------
# 2. VEDIC MATH
# ---------------------------------------------------------

NAKSHATRAS = [
    "Ashvini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purvaphalguni", "Uttaraphalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
    "Purvashadha", "Uttarashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purvabhadra", "Uttarabhadra", "Revati"
]

DASHA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17] # Total 120

def get_nakshatra(lon):
    # 360 / 27 = 13.3333... degrees per Nakshatra
    # 13 degrees 20 minutes
    one_nak = 13 + (20/60)
    idx = int(lon / one_nak)
    percent_traversed = (lon % one_nak) / one_nak
    return idx, percent_traversed

def calculate_dasha(moon_lon_sidereal, birth_dt_utc):
    """
    Vimshottari Dasha Calculation.
    """
    nak_idx, percent = get_nakshatra(moon_lon_sidereal)
    
    # Starting Lord
    # Cycle starts at Ashvini (Ketu).
    # Nakshatra 0 (Ashvini) -> Ketu
    # Nakshatra 1 (Bharani) -> Venus
    # ...
    # Pattern repeats every 9 nakshatras.
    lord_idx = nak_idx % 9
    start_lord = DASHA_LORDS[lord_idx]
    duration = DASHA_YEARS[lord_idx]
    
    # Balance of Dasha
    # If percent traversed is 0.5, then 50% of dasha is passed. 50% remaining.
    remaining_fraction = 1.0 - percent
    balance_years = duration * remaining_fraction
    
    # Generate Timeline
    md = "# 09 DASHA TIMELINE (VIMSHOTTARI)\n\n"
    md += f"**Birth:** {birth_dt_utc.strftime('%Y-%m-%d')}\n"
    md += f"**Moon Nakshatra:** {NAKSHATRAS[nak_idx]}\n"
    md += f"**Starting Dasha:** {start_lord}\n"
    md += f"**Balance:** {balance_years:.2f} years\n"
    md += "---\n\n"
    md += "| Dasha (Mahadasha) | Start Date | Age |\n"
    md += "|:---|:---|:---|\n"
    
    # 1. End of first dasha
    current_date = birth_dt_utc + datetime.timedelta(days=balance_years*365.25)
    age = balance_years
    
    # List first dasha entry (Start is Birth)
    md += f"| **{start_lord}** | Birth | 0.0 |\n"
    
    # Loop through next lords
    curr_lord_idx = (lord_idx + 1) % 9
    
    for i in range(9): # One full cycle (120 years)
        lord = DASHA_LORDS[curr_lord_idx]
        years = DASHA_YEARS[curr_lord_idx]
        
        start_date_str = current_date.strftime('%Y-%m-%d')
        md += f"| **{lord}** | {start_date_str} | {age:.1f} |\n"
        
        current_date += datetime.timedelta(days=years*365.25)
        age += years
        curr_lord_idx = (curr_lord_idx + 1) % 9
        
    return md

def calculate_varga(lon, div_num):
    """
    Generalized Varga Calculator.
    D9 = Navamsa.
    """
    # 1. Arc in Sign
    sign_deg = lon % 30
    
    # 2. Sector Size
    sector = 30.0 / div_num
    
    # 3. Sector Index (0 to div_num-1)
    idx = int(sign_deg / sector)
    
    # 4. Mapping Logic (Complex for each Varga)
    # D9 Standard (Parasara):
    # Fire signs (1,5,9) start Aries
    # Earth signs (2,6,10) start Capricorn
    # Air signs (3,7,11) start Libra
    # Water signs (4,8,12) start Cancer
    
    sign_idx = int(lon / 30) # 0 = Aries
    
    if div_num == 9:
        # Standard Navamsa
        # Normalize sign index to 1-12
        s = sign_idx + 1
        start_sign = 0
        
        if s in [1, 5, 9]: start_sign = 0 # Aries
        elif s in [2, 6, 10]: start_sign = 9 # Capricorn
        elif s in [3, 7, 11]: start_sign = 6 # Libra
        elif s in [4, 8, 12]: start_sign = 3 # Cancer
        
        # Add index
        final_sign_idx = (start_sign + idx) % 12
        
        # Degree in Varga?
        # Typically treated as a new chart.
        # Degree = (sign_deg % sector) * div_num
        final_deg = (sign_deg % sector) * div_num
        
        return final_sign_idx, final_deg
        
    # TODO: Implement D10, D7 etc if needed.
    # Default to just D9 for now as it's the most critical.
    return sign_idx, sign_deg

def get_sign_name(idx):
    signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
    return signs[idx]

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    date_str, time_str, tz_offset, lat, lon = parse_core_data()
    
    # Convert DT to UTC
    # Simple hack: Subtract offset
    dt_str = f"{date_str} {time_str}"
    d = datetime.datetime.strptime(dt_str, "%Y/%m/%d %H:%M")
    
    # Parse offset "+03:00"
    h_off = int(tz_offset.split(':')[0])
    m_off = int(tz_offset.split(':')[1])
    
    # UTC Time
    utc_dt = d - datetime.timedelta(hours=h_off, minutes=m_off)
    
    # Julian Day
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
    
    # Set Sidereal
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    
    # Calculate Planets
    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE # Mean or True? Using Mean for traditional
    }
    
    results = {}
    
    # 06_VEDIC_DETAILS.md content
    md_det = "# 06 VEDIC DETAILS (EXTENDED)\n\n"
    md_det += "| Planet | Sidereal Pos | Nakshatra |\n"
    md_det += "|:---|:---|:---|\n"
    
    for name, pid in planets.items():
        res = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)
        # res is usually ((lon, lat, dist, speed...), flags) in some implementations
        # or just (lon, lat...)
        if len(res) == 2 and isinstance(res[0], tuple):
             lon_val = res[0][0]
        else:
             lon_val = res[0]
             
        results[name] = lon_val
        
        # Nakshatra
        nak, perc = get_nakshatra(lon_val)
        
        # Sign
        s_idx = int(lon_val / 30)
        deg = lon_val % 30
        
        md_det += f"| **{name}** | {get_sign_name(s_idx)} {int(deg)}° | {NAKSHATRAS[nak]} ({perc*100:.1f}%) |\n"
        
    with open(OUTPUT_DETAILS, 'w') as f: f.write(md_det)
    
    # 09_DASHA.md
    md_dasha = calculate_dasha(results['Moon'], utc_dt)
    with open(OUTPUT_DASHA, 'w') as f: f.write(md_dasha)
    
    # 10_DIVISIONALS.md (D9)
    md_div = "# 10 DIVISIONAL CHARTS (VARGAS)\n\n"
    md_div += "## D9 (Navamsa) - Fruit of the Tree\n"
    md_div += "| Planet | D9 Sign |\n"
    md_div += "|:---|:---|\n"
    
    for name, lon_val in results.items():
        s_idx, deg = calculate_varga(lon_val, 9)
        md_div += f"| **{name}** | {get_sign_name(s_idx)} |\n"
        
    with open(OUTPUT_VARGA, 'w') as f: f.write(md_div)
    
    print("Done. Check 'scratches/sessions/001_Refine_Coordinates/'")

if __name__ == "__main__":
    main()
