
import sys
import datetime
import re
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

# USER DATA (UPDATED 2026-01-27)
BIRTH_DATE = Datetime('2007/04/24', '01:15', '+00:00') # 04:15 EEST -> 01:15 UTC
POS = GeoPos('46n58', '28e52') # 46.9809, 28.8704
OUTPUT_FILE = "cases/001_Theodore/00_CORE_DATA/03_TRANSITS.md"

if len(sys.argv) > 1:
    OUTPUT_DIR = sys.argv[1]
    OUTPUT_FILE = f"{OUTPUT_DIR}/TEST_03_TRANSITS.md"


def get_orb_str(orb):
    d = int(orb)
    m = int((orb - d) * 60)
    return f"{d}°{m:02d}'"

def get_transits():
    # 1. SETUP TIME
    now_utc = datetime.datetime.utcnow()
    date_str = now_utc.strftime('%Y/%m/%d')
    time_str = now_utc.strftime('%H:%M')
    transit_date = Datetime(date_str, time_str, '+00:00')

    # 2. GENERATE CHARTS
    # Tropical
    natal_trop = Chart(BIRTH_DATE, POS, IDs=const.LIST_OBJECTS)
    transit_trop = Chart(transit_date, POS, IDs=const.LIST_OBJECTS)
    
    # Sidereal (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    ayanamsa = swe.get_ayanamsa_ut(transit_date.jd)

    # Draconic (North Node)
    nn = natal_trop.get(const.NORTH_NODE)
    nn_lon = nn.lon

    # Objects to scan
    objects = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
        const.NORTH_NODE
    ]
    
    output = f"# 03 TRANSITS (THE WEATHER)\n\n"
    output += f"**Updated:** {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    output += f"**Ayanamsa:** {ayanamsa:.4f}° | **Draconic NN:** {nn_lon:.4f}°\n"
    output += "---\n\n"

    # ---------------------------------------------------------
    # PART 1: TROPICAL IMPACT (Western)
    # ---------------------------------------------------------
    output += "## 1. TROPICAL IMPACT (WESTERN)\n"
    output += "| Transit | Aspect | Natal | Orb |\n"
    output += "|:---|:---|:---|:---|\n"
    
    matches = 0
    match_list = []
    
    for t_obj in objects:
        t_p = transit_trop.get(t_obj)
        for n_obj in objects:
            n_p = natal_trop.get(n_obj)
            
            try:
                aspect = aspects.getAspect(t_p, n_p, const.MAJOR_ASPECTS)
            except: continue
            
            if aspect.exists() and aspect.orb < 1.0:
                matches += 1
                orb_str = get_orb_str(aspect.orb)
                weight = "**" if aspect.orb < 0.2 else ""
                match_list.append(f"| **{t_obj}** | {aspect.type} | **{n_obj}** | {weight}{orb_str}{weight} |")
    
    if match_list:
        output += "\n".join(match_list) + "\n"
    else:
        output += "| -- | -- | -- | -- |\n"
        output += "*No Nuclear Events (<1°)*\n"

    # ---------------------------------------------------------
    # PART 2: SIDEREAL IMPACT (Vedic)
    # ---------------------------------------------------------
    output += "\n## 2. SIDEREAL IMPACT (VEDIC)\n"
    output += "| Transit | Aspect | Natal | Orb |\n"
    output += "|:---|:---|:---|:---|\n"
    
    # Manual Sidereal check because aspect logic is same absolute distance
    # But Signs change. We just list verified matches.
    # Actually, aspect orb doesn't change between Tropical/Sidereal unless dealing with sign-based aspects.
    # But planetary positions in signs change.
    # We will just list the Sidereal sign of the transiting planet for context.
    
    sid_matches = []
    signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
    
    for t_obj in objects:
        t_p_trop = transit_trop.get(t_obj)
        t_sid_lon = (t_p_trop.lon - ayanamsa) % 360
        t_sign = signs[int(t_sid_lon // 30)]
        
        for n_obj in objects:
            n_p_trop = natal_trop.get(n_obj)
            # Aspect calculation is identical in absolute longitude
            try:
                aspect = aspects.getAspect(t_p_trop, n_p_trop, const.MAJOR_ASPECTS)
            except: continue

            if aspect.exists() and aspect.orb < 1.0:
                # But we verify it relative to Sidereal just to be safe? No, math is math.
                # Just report it with Sidereal context.
                orb_str = get_orb_str(aspect.orb)
                weight = "**" if aspect.orb < 0.2 else ""
                sid_matches.append(f"| **{t_obj}** ({t_sign}) | {aspect.type} | **{n_obj}** | {weight}{orb_str}{weight} |")

    if sid_matches:
        output += "\n".join(sid_matches) + "\n"
    else:
        output += "| -- | -- | -- | -- |\n"

    # ---------------------------------------------------------
    # PART 3: DRACONIC IMPACT (Soul)
    # ---------------------------------------------------------
    output += "\n## 3. DRACONIC IMPACT (SOUL)\n"
    output += "| Transit | Aspect | Natal | Orb |\n"
    output += "|:---|:---|:---|:---|\n"
    
    # Draconic = Tropical - NN.
    # If we compare Draconic to Draconic, the relative angle is exact same as Tropical to Tropical.
    # UNLESS we compare Transiting Draconic to Natal Tropical (Cross-Dimensional).
    # Usually "Draconic Transits" implies Transiting Draconic vs Natal Draconic.
    # Which is mathematically identical to Tropical vs Tropical aspects.
    # So repeating it is redundant unless we do Cross-Dimension.
    # Let's assume standard Draconic vs Draconic is same as Tropical.
    # Let's do **Transiting Tropical vs Natal Draconic** (World hits Soul).
    
    drac_matches = []
    
    for t_obj in objects:
        t_p_trop = transit_trop.get(t_obj)
        
        for n_obj in objects:
            n_p_trop = natal_trop.get(n_obj)
            n_drac_lon = (n_p_trop.lon - nn_lon) % 360
            
            # Create a dummy object for aspect calc
            # We can't easily create a flatlib object with arbitrary lon without hack
            # So simple math diff
            diff = abs(t_p_trop.lon - n_drac_lon)
            if diff > 180: diff = 360 - diff
            
            aspect_type = ""
            orb = 0
            
            if diff < 1.0: 
                aspect_type = "Conjunct"
                orb = diff
            elif abs(diff - 180) < 1.0:
                aspect_type = "Opposition"
                orb = abs(diff - 180)
            elif abs(diff - 90) < 1.0:
                aspect_type = "Square"
                orb = abs(diff - 90)
            elif abs(diff - 120) < 1.0:
                aspect_type = "Trine"
                orb = abs(diff - 120)

            if aspect_type:
                orb_str = get_orb_str(orb)
                weight = "**" if orb < 0.2 else ""
                drac_matches.append(f"| **{t_obj}** (Trop) | {aspect_type} | **{n_obj}** (Drac) | {weight}{orb_str}{weight} |")

    if drac_matches:
        output += "\n".join(drac_matches) + "\n"
    else:
        output += "| -- | -- | -- | -- |\n"
        output += "*No Cross-Dimensional Hits*\n"

    # WRITE TO FILE
    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)
    
    print(f"Successfully updated {OUTPUT_FILE}")

if __name__ == "__main__":
    get_transits()
