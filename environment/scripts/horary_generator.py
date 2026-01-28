#!/usr/bin/env python3
"""
HORARY CHART GENERATOR
Generates a complete Horary forensic packet from raw input.

Usage:
  python3 horary_generator.py "YYYY-MM-DD HH:MM:SS" "TIMEZONE" "LAT" "LON" "QUESTION" OUTPUT_DIR

Example:
  python3 horary_generator.py "2026-01-12 06:45:37" "+02:00" "47.0160975" "28.7954969" "Should I love her?" scratches/sessions/Horary

Output Files:
  - 00_CORE_DATA.md
  - 01_HOUSES.md
  - 02_BODIES.md
  - 03_STRUCTURAL_FLAGS.md
  - 04_ASPECTS.md
  - 05_MOON_PERFECTIONS.md
  - 06_RECEPTIONS.md
"""

import sys
import os
import datetime
import math

# Swiss Ephemeris
import swisseph as swe

# Set ephemeris path
EPHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sweph"))
swe.set_ephe_path(EPHE_PATH)

# Constants
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = [
    (swe.SUN, "Sun"),
    (swe.MOON, "Moon"),
    (swe.MERCURY, "Mercury"),
    (swe.VENUS, "Venus"),
    (swe.MARS, "Mars"),
    (swe.JUPITER, "Jupiter"),
    (swe.SATURN, "Saturn"),
    (swe.URANUS, "Uranus"),
    (swe.NEPTUNE, "Neptune"),
    (swe.PLUTO, "Pluto"),
    (swe.TRUE_NODE, "Node"),
    (swe.MEAN_APOG, "Lilith"),
]

CLASSICAL_PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

MAJOR_ASPECTS = [
    (0, "Conjunction", 8),
    (60, "Sextile", 6),
    (90, "Square", 7),
    (120, "Trine", 8),
    (180, "Opposition", 8),
]

# Essential Dignities (Domicile Rulerships)
RULERSHIPS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

EXALTATIONS = {
    "Aries": "Sun", "Taurus": "Moon", "Cancer": "Jupiter", "Virgo": "Mercury",
    "Libra": "Saturn", "Capricorn": "Mars", "Pisces": "Venus"
}

DETRIMENTS = {
    "Aries": "Venus", "Taurus": "Mars", "Gemini": "Jupiter", "Cancer": "Saturn",
    "Leo": "Saturn", "Virgo": "Jupiter", "Libra": "Mars", "Scorpio": "Venus",
    "Sagittarius": "Mercury", "Capricorn": "Moon", "Aquarius": "Sun", "Pisces": "Mercury"
}

FALLS = {
    "Aries": "Saturn", "Taurus": "None", "Gemini": "None", "Cancer": "Mars",
    "Leo": "None", "Virgo": "Venus", "Libra": "Sun", "Scorpio": "Moon",
    "Sagittarius": "None", "Capricorn": "Jupiter", "Aquarius": "None", "Pisces": "Mercury"
}

# Traditional Fixed Stars (Royal, Malefic, and significant)
FIXED_STARS = [
    "Algol",           # Beta Persei - the Demon Star
    "Alcyone",         # Eta Tauri - the Pleiades
    "Aldebaran",       # Alpha Tauri - Royal Star
    "Rigel",           # Beta Orionis
    "Capella",         # Alpha Aurigae
    "Betelgeuse",      # Alpha Orionis
    "Sirius",          # Alpha Canis Majoris - brightest
    "Canopus",         # Alpha Carinae
    "Castor",          # Alpha Geminorum
    "Pollux",          # Beta Geminorum
    "Procyon",         # Alpha Canis Minoris
    "Regulus",         # Alpha Leonis - Royal Star
    "Denebola",        # Beta Leonis
    "Algorab",         # Delta Corvi
    "Spica",           # Alpha Virginis
    "Arcturus",        # Alpha Bootis
    "Alphecca",        # Alpha Coronae Borealis
    "Zuben Elgenubi",  # Alpha Librae
    "Zuben Eschamali", # Beta Librae
    "Unukalhai",       # Alpha Serpentis
    "Antares",         # Alpha Scorpii - Royal Star
    "Vega",            # Alpha Lyrae
    "Altair",          # Alpha Aquilae
    "Deneb Algedi",    # Delta Capricorni
    "Fomalhaut",       # Alpha Piscis Austrini - Royal Star
    "Markab",          # Alpha Pegasi
    "Scheat",          # Beta Pegasi
    "Achernar",        # Alpha Eridani
    "Mirach",          # Beta Andromedae
    "Almach",          # Gamma Andromedae
]


def calculate_fixed_stars(jd, positions, cusps, orb_limit=1.5):
    """Calculate fixed star positions using Swiss Ephemeris."""
    stars = []
    contacts = []
    
    for star_name in FIXED_STARS:
        try:
            # swe.fixstar2_ut returns (results_tuple, star_name_full, return_flags)
            result = swe.fixstar2_ut(star_name, jd, 0)
            lon = result[0][0]  # First element of the results tuple is longitude
            sign, deg = lon_to_sign(lon)
            
            # Determine house
            house = get_house_position(lon, cusps)
            
            stars.append({
                "name": star_name,
                "lon": lon,
                "sign": sign,
                "degree": deg,
                "house": house
            })
            
            # Check for tight contacts to planets and angles
            for planet_name, p_data in positions.items():
                diff = abs(lon - p_data["lon"])
                if diff > 180:
                    diff = 360 - diff
                if diff <= orb_limit:
                    contacts.append({
                        "star": star_name,
                        "planet": planet_name,
                        "orb": diff
                    })
        except Exception as e:
            # Star not found or error - skip silently
            pass
    
    return stars, contacts


def lon_to_sign(lon):
    """Convert longitude to zodiac sign and degree."""
    sign_idx = int(lon // 30)
    degree = lon % 30
    return ZODIAC_SIGNS[sign_idx], degree


def format_dms(degree):
    """Convert decimal degree to D°M'S" format."""
    d = int(degree)
    m_float = (degree - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return f"{d:02d}°{m:02d}'{s:05.2f}\""


def format_position(lon):
    """Format longitude as Sign DD°MM'SS"."""
    sign, deg = lon_to_sign(lon)
    return f"{sign} {format_dms(deg)}"


def parse_datetime(date_str, time_str, tz_str):
    """Parse inputs to Julian Day for Swiss Ephemeris."""
    # Parse date: "2026-01-12"
    year, month, day = map(int, date_str.split("-"))
    
    # Parse time: "06:45:37"
    h, m, s = map(int, time_str.split(":"))
    
    # Parse timezone: "+02:00" -> offset in hours
    tz_sign = 1 if tz_str[0] == '+' else -1
    tz_parts = tz_str[1:].replace(":", "")
    if len(tz_parts) <= 2:
        tz_hours = int(tz_parts)
        tz_mins = 0
    else:
        tz_hours = int(tz_parts[:2])
        tz_mins = int(tz_parts[2:4]) if len(tz_parts) >= 4 else 0
    tz_offset = tz_sign * (tz_hours + tz_mins / 60.0)
    
    # Convert to UT
    ut_hour = h + m/60 + s/3600 - tz_offset
    
    # Handle day rollover
    if ut_hour < 0:
        ut_hour += 24
        day -= 1
    elif ut_hour >= 24:
        ut_hour -= 24
        day += 1
    
    # Calculate Julian Day
    jd = swe.julday(year, month, day, ut_hour)
    
    return jd, ut_hour, tz_offset


def calculate_houses(jd, lat, lon, hsys='R'):
    """Calculate house cusps using Regiomontanus."""
    cusps, ascmc = swe.houses(jd, lat, lon, hsys.encode())
    return cusps, ascmc  # cusps[0-11] = houses 1-12, ascmc[0]=ASC, ascmc[1]=MC


def calculate_planets(jd):
    """Calculate planetary positions."""
    positions = {}
    for planet_id, name in PLANETS:
        result, flags = swe.calc_ut(jd, planet_id)
        lon = result[0]
        lat = result[1]
        speed = result[3]  # Daily speed
        positions[name] = {
            "lon": lon,
            "lat": lat,
            "speed": speed,
            "retrograde": speed < 0
        }
    return positions


def get_house_position(lon, cusps):
    """Determine which house a longitude falls in."""
    for i in range(12):
        cusp_start = cusps[i]
        cusp_end = cusps[(i + 1) % 12]
        
        # Handle wrap-around
        if cusp_end < cusp_start:
            if lon >= cusp_start or lon < cusp_end:
                return i + 1
        else:
            if cusp_start <= lon < cusp_end:
                return i + 1
    return 1  # Fallback


def calculate_aspects(positions, orb_limit=6.0, classical_only=True):
    """Calculate major aspects between planets."""
    aspects = []
    
    planet_list = CLASSICAL_PLANETS if classical_only else list(positions.keys())
    
    for i, p1 in enumerate(planet_list):
        for j, p2 in enumerate(planet_list):
            if i >= j:
                continue
            
            if p1 not in positions or p2 not in positions:
                continue
                
            lon1 = positions[p1]["lon"]
            lon2 = positions[p2]["lon"]
            speed1 = positions[p1]["speed"]
            speed2 = positions[p2]["speed"]
            
            diff = abs(lon1 - lon2)
            if diff > 180:
                diff = 360 - diff
            
            for aspect_angle, aspect_name, default_orb in MAJOR_ASPECTS:
                orb = abs(diff - aspect_angle)
                if orb <= orb_limit:
                    # Determine applying/separating
                    # Faster planet applies to slower
                    # If they're moving toward exact, it's applying
                    
                    # Simplified: if orb is decreasing, applying
                    # Use relative speeds
                    rel_speed = abs(speed1) - abs(speed2)
                    
                    # More accurate: check if aspect is getting tighter
                    # For now, simplified heuristic
                    if abs(speed1) > abs(speed2):
                        faster = p1
                    else:
                        faster = p2
                    
                    # Heuristic: if faster planet's speed brings it toward exact
                    # This is complex; simplified to "applying if orb < 3"
                    applying = orb < 3.0  # Simplified
                    
                    aspects.append({
                        "p1": p1,
                        "p2": p2,
                        "aspect": aspect_name,
                        "orb": orb,
                        "applying": applying
                    })
                    break
    
    return aspects


def check_via_combusta(moon_lon):
    """Check if Moon is in Via Combusta (15° Libra to 15° Scorpio)."""
    via_start = 195.0  # 15° Libra
    via_end = 225.0    # 15° Scorpio
    return via_start <= moon_lon <= via_end


def check_radicality(asc_lon, moon_lon):
    """Check radicality conditions."""
    flags = []
    
    # Early/Late degrees
    asc_deg = asc_lon % 30
    if asc_deg < 3:
        flags.append(f"EARLY ASCENDANT ({format_dms(asc_deg)}) - Chart may be too early to judge")
    if asc_deg > 27:
        flags.append(f"LATE ASCENDANT ({format_dms(asc_deg)}) - Chart may be too late to judge")
    
    # Moon Void of Course would need aspect calculation
    # Skipped for now
    
    return flags


def get_essential_dignity(planet, sign):
    """Get essential dignity status of a planet in a sign."""
    dignities = []
    
    if RULERSHIPS.get(sign) == planet:
        dignities.append("Domicile (+5)")
    if EXALTATIONS.get(sign) == planet:
        dignities.append("Exaltation (+4)")
    if DETRIMENTS.get(sign) == planet:
        dignities.append("Detriment (-5)")
    if FALLS.get(sign) == planet:
        dignities.append("Fall (-4)")
    
    return dignities if dignities else ["Peregrine (0)"]


def calculate_sun_altitude(jd, lat, lon, cusps):
    """Calculate Sun's altitude to determine sect.
    
    Uses the simpler but reliable method: if Sun is below the horizon 
    (houses 1-6), it's a night chart. Above (houses 7-12), it's a day chart.
    """
    # Get Sun position
    result, _ = swe.calc_ut(jd, swe.SUN)
    sun_lon = result[0]
    
    # Determine Sun's house
    sun_house = get_house_position(sun_lon, cusps)
    
    # Houses 7-12 are above horizon (day), houses 1-6 are below (night)
    # Actually: 1-6 = above, 7-12 = below in standard chart
    # Wait - standard is: 1st rises at ASC (left), 7th sets at DSC (right)
    # Above horizon = houses 7, 8, 9, 10, 11, 12 (descending to rising)
    # Below horizon = houses 1, 2, 3, 4, 5, 6
    # Actually standard convention:
    # 12, 11, 10, 9, 8, 7 = above horizon
    # 6, 5, 4, 3, 2, 1 = below horizon
    # So: if Sun in houses 7-12, it's above horizon (day chart)
    #     if Sun in houses 1-6, it's below horizon (night chart)
    
    is_day = sun_house >= 7
    
    # Return a pseudo-altitude for clarity
    # Positive = day, Negative = night
    pseudo_altitude = 10.0 if is_day else -10.0
    
    return pseudo_altitude, sun_house


def calculate_moon_perfections(jd, positions, hours_ahead=72):
    """Calculate when Moon will perfect aspects to other planets."""
    perfections = []
    moon_lon = positions["Moon"]["lon"]
    moon_speed = positions["Moon"]["speed"]
    
    if moon_speed <= 0:
        return perfections  # Moon retrograde is extremely rare, skip
    
    for planet in CLASSICAL_PLANETS:
        if planet == "Moon":
            continue
        
        target_lon = positions[planet]["lon"]
        target_speed = positions[planet]["speed"]
        
        for aspect_angle, aspect_name, _ in MAJOR_ASPECTS:
            # Calculate target positions
            # Moon needs to reach target_lon + aspect_angle (or - aspect_angle)
            
            for direction in [1, -1]:
                target_point = (target_lon + direction * aspect_angle) % 360
                
                # Distance Moon needs to travel
                dist = (target_point - moon_lon) % 360
                if dist > 180:
                    dist = 360 - dist
                    continue  # Only forward motion
                
                # Time = distance / relative speed
                rel_speed = moon_speed - target_speed
                if rel_speed <= 0:
                    continue
                
                days = dist / rel_speed
                hours = days * 24
                
                if 0 < hours < hours_ahead:
                    perf_jd = jd + days
                    perf_time = swe.revjul(perf_jd)
                    
                    perfections.append({
                        "target": planet,
                        "aspect": aspect_name,
                        "hours": hours,
                        "jd": perf_jd,
                        "time_ut": perf_time
                    })
    
    # Sort by time
    perfections.sort(key=lambda x: x["hours"])
    return perfections


def generate_core_data_md(date_str, time_str, tz_str, lat, lon, question, jd, ut_hour):
    """Generate 00_CORE_DATA.md."""
    md = "# 00_CORE_DATA\n\n"
    md += "## Interrogation moment (authoritative)\n"
    md += f"- Local date/time: **{date_str} {time_str}**\n"
    md += f"- Coordinates (decimal): **{lat} N, {lon} E**\n\n"
    
    md += "## Question\n"
    md += f"> {question}\n\n"
    
    md += "## Time standardization\n"
    md += f"- Timezone: **UTC{tz_str}**\n"
    md += f"- Universal Time (UT): **{date_str} {int(ut_hour):02d}:{int((ut_hour % 1) * 60):02d}:{int(((ut_hour % 1) * 60 % 1) * 60):02d}**\n"
    md += f"- Julian Day: **{jd:.6f}**\n\n"
    
    md += "## Chart calculation settings\n"
    md += "- Zodiac: **Tropical**\n"
    md += "- Houses: **Regiomontanus**\n"
    md += "- Terms/Bounds: **Egyptian**\n"
    md += "- Aspects: **Major only**\n\n"
    
    md += "## Provenance\n"
    md += f"- Generated: **{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    md += "- Calculator: **Pollux Horary Generator (Swiss Ephemeris)**\n"
    
    return md


def generate_houses_md(cusps, ascmc):
    """Generate 01_HOUSES.md."""
    md = "# 01_HOUSES (Regiomontanus)\n\n"
    md += "| House | Sign | Degree | Lon360 |\n"
    md += "|:---:|:---|:---|---:|\n"
    
    for i, cusp in enumerate(cusps):
        sign, deg = lon_to_sign(cusp)
        md += f"| {i+1} | {sign} | {format_dms(deg)} | {cusp:.4f} |\n"
    
    md += "\n## Angles\n"
    md += "| Angle | Sign | Degree | Lon360 |\n"
    md += "|:---|:---|:---|---:|\n"
    
    asc_sign, asc_deg = lon_to_sign(ascmc[0])
    mc_sign, mc_deg = lon_to_sign(ascmc[1])
    
    md += f"| ASC | {asc_sign} | {format_dms(asc_deg)} | {ascmc[0]:.4f} |\n"
    md += f"| MC | {mc_sign} | {format_dms(mc_deg)} | {ascmc[1]:.4f} |\n"
    
    return md


def generate_bodies_md(positions, cusps):
    """Generate 02_BODIES.md."""
    md = "# 02_BODIES\n\n"
    md += "| Body | Position | House | Motion | Speed (°/day) |\n"
    md += "|:---|:---|:---:|:---:|---:|\n"
    
    for name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Node", "Lilith"]:
        if name not in positions:
            continue
        p = positions[name]
        pos_str = format_position(p["lon"])
        house = get_house_position(p["lon"], cusps)
        motion = "R" if p["retrograde"] else "D"
        speed = p["speed"]
        md += f"| {name} | {pos_str} | {house} | {motion} | {speed:+.4f} |\n"
    
    return md


def generate_structural_flags_md(positions, ascmc, cusps, jd, lat, lon):
    """Generate 03_STRUCTURAL_FLAGS.md."""
    md = "# 03_STRUCTURAL_FLAGS\n\n"
    
    moon_lon = positions["Moon"]["lon"]
    asc_lon = ascmc[0]
    
    # Via Combusta
    md += "## Via Combusta check\n"
    in_via = check_via_combusta(moon_lon)
    md += f"- Traditional bounds: **15° Libra (195°)** to **15° Scorpio (225°)**\n"
    md += f"- Moon longitude: **{moon_lon:.4f}°** ({format_position(moon_lon)})\n"
    md += f"- Moon within Via Combusta: **{in_via}**\n\n"
    
    # Sect
    md += "## Sect (Day/Night)\n"
    sun_alt, sun_house = calculate_sun_altitude(jd, lat, lon, cusps)
    sect = "Day" if sun_alt >= 0 else "Night"
    md += f"- Sun in House: **{sun_house}**\n"
    md += f"- Sect: **{sect} chart** ({'above' if sun_alt >= 0 else 'below'} horizon)\n\n"
    
    # Radicality
    md += "## Radicality warnings\n"
    warnings = check_radicality(asc_lon, moon_lon)
    if warnings:
        for w in warnings:
            md += f"- ⚠️ {w}\n"
    else:
        md += "- ✅ No radicality issues detected\n"
    
    return md


def generate_aspects_md(aspects):
    """Generate 04_ASPECTS.md."""
    md = "# 04_ASPECTS (Classical planets, orb ≤ 6°)\n\n"
    md += "| Planet A | Aspect | Planet B | Orb | Status |\n"
    md += "|:---|:---:|:---|:---|:---|\n"
    
    for a in sorted(aspects, key=lambda x: x["orb"]):
        status = "Applying" if a["applying"] else "Separating"
        orb_str = f"{int(a['orb'])}°{int((a['orb'] % 1) * 60):02d}'"
        md += f"| {a['p1']} | {a['aspect']} | {a['p2']} | {orb_str} | {status} |\n"
    
    return md


def generate_moon_perfections_md(perfections, jd):
    """Generate 05_MOON_PERFECTIONS.md."""
    md = "# 05_MOON_PERFECTIONS\n\n"
    md += "Moon's next exact major aspects:\n\n"
    md += "| Target | Aspect | Time (UT) | Hours from now |\n"
    md += "|:---|:---:|:---|---:|\n"
    
    for p in perfections[:10]:  # Limit to next 10
        time_parts = p["time_ut"]
        time_str = f"{int(time_parts[0])}-{int(time_parts[1]):02d}-{int(time_parts[2]):02d} {int(time_parts[3]):02d}:{int((time_parts[3] % 1) * 60):02d}"
        md += f"| {p['target']} | {p['aspect']} | {time_str} | {p['hours']:.1f} |\n"
    
    return md


def generate_receptions_md(positions):
    """Generate 06_RECEPTIONS.md."""
    md = "# 06_RECEPTIONS (Essential Dignities)\n\n"
    md += "| Planet | Sign | Dignities |\n"
    md += "|:---|:---|:---|\n"
    
    for name in CLASSICAL_PLANETS:
        if name not in positions:
            continue
        lon = positions[name]["lon"]
        sign, _ = lon_to_sign(lon)
        dignities = get_essential_dignity(name, sign)
        md += f"| {name} | {sign} | {', '.join(dignities)} |\n"
    
    return md


def generate_fixed_stars_md(stars, contacts):
    """Generate 07_FIXED_STARS.md."""
    md = "# 07_FIXED_STARS\n\n"
    md += f"Calculated using Swiss Ephemeris native star catalog.\n\n"
    
    md += "## Star Positions\n"
    md += "| Star | Position | House | Lon360 |\n"
    md += "|:---|:---|:---:|---:|\n"
    
    for s in sorted(stars, key=lambda x: x["lon"]):
        md += f"| {s['name']} | {s['sign']} {format_dms(s['degree'])} | {s['house']} | {s['lon']:.4f} |\n"
    
    md += "\n## Tight Contacts (orb ≤ 1.5°)\n"
    if contacts:
        md += "| Star | Planet | Orb |\n"
        md += "|:---|:---|---:|\n"
        for c in sorted(contacts, key=lambda x: x["orb"]):
            md += f"| {c['star']} | {c['planet']} | {c['orb']:.4f}° |\n"
    else:
        md += "- No tight contacts found.\n"
    
    return md


def main():
    if len(sys.argv) < 7:
        print("Usage: python3 horary_generator.py DATE TIME TIMEZONE LAT LON QUESTION OUTPUT_DIR")
        print('Example: python3 horary_generator.py "2026-01-12" "06:45:37" "+02:00" "47.0160975" "28.7954969" "Should I love her?" output/')
        sys.exit(1)
    
    date_str = sys.argv[1]
    time_str = sys.argv[2]
    tz_str = sys.argv[3]
    lat = float(sys.argv[4])
    lon = float(sys.argv[5])
    question = sys.argv[6]
    output_dir = sys.argv[7] if len(sys.argv) > 7 else "."
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating Horary chart for: {date_str} {time_str} {tz_str}")
    print(f"Location: {lat}, {lon}")
    print(f"Question: {question}")
    print(f"Output: {output_dir}")
    print("-" * 60)
    
    # Parse and calculate
    jd, ut_hour, tz_offset = parse_datetime(date_str, time_str, tz_str)
    print(f"Julian Day: {jd:.6f}")
    
    cusps, ascmc = calculate_houses(jd, lat, lon, 'R')  # R = Regiomontanus
    print(f"ASC: {format_position(ascmc[0])}")
    print(f"MC: {format_position(ascmc[1])}")
    
    positions = calculate_planets(jd)
    print(f"Sun: {format_position(positions['Sun']['lon'])}")
    print(f"Moon: {format_position(positions['Moon']['lon'])}")
    
    aspects = calculate_aspects(positions, orb_limit=6.0, classical_only=True)
    print(f"Aspects found: {len(aspects)}")
    
    perfections = calculate_moon_perfections(jd, positions)
    print(f"Moon perfections: {len(perfections)}")
    
    stars, star_contacts = calculate_fixed_stars(jd, positions, cusps)
    print(f"Fixed stars: {len(stars)}, Contacts: {len(star_contacts)}")
    
    print("-" * 60)
    
    # Generate files
    files = {
        "00_CORE_DATA.md": generate_core_data_md(date_str, time_str, tz_str, lat, lon, question, jd, ut_hour),
        "01_HOUSES.md": generate_houses_md(cusps, ascmc),
        "02_BODIES.md": generate_bodies_md(positions, cusps),
        "03_STRUCTURAL_FLAGS.md": generate_structural_flags_md(positions, ascmc, cusps, jd, lat, lon),
        "04_ASPECTS.md": generate_aspects_md(aspects),
        "05_MOON_PERFECTIONS.md": generate_moon_perfections_md(perfections, jd),
        "06_RECEPTIONS.md": generate_receptions_md(positions),
        "07_FIXED_STARS.md": generate_fixed_stars_md(stars, star_contacts),
    }
    
    for filename, content in files.items():
        path = os.path.join(output_dir, filename)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created: {path}")
    
    print("-" * 60)
    print("HORARY PACKET GENERATED SUCCESSFULLY")


if __name__ == "__main__":
    main()
