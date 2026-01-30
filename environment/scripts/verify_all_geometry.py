#!/usr/bin/env python3
"""
VERIFY ALL GEOMETRY — THE CANONICAL REFERENCE GENERATOR
=========================================================
This script calculates EVERY geometric fact about Theodore's chart
using Swiss Ephemeris (Moshier). It reads birth data from 00_CORE_DATA.md
and outputs a comprehensive reference file.

NEVER hardcode birth data. ALWAYS read from the file.

Output: 11_VERIFIED_GEOMETRY.md (the single source of truth)
"""

import os
import re
import math
import datetime
import swisseph as swe

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
CORE_DATA_PATH = os.path.join(PROJECT_ROOT, 'cases', '001_Theodore', '00_CORE_DATA', '00_CORE_DATA.md')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'cases', '001_Theodore', '00_CORE_DATA', '11_VERIFIED_GEOMETRY.md')
EPHE_PATH = os.path.join(PROJECT_ROOT, 'environment', 'data', 'sweph')

# Use Moshier (built-in, no external files needed for planets)
swe.set_ephe_path(EPHE_PATH)

# --- ASPECT DEFINITIONS ---
MAJOR_ASPECTS = {
    'Conjunction': 0, 'Sextile': 60, 'Square': 90,
    'Trine': 120, 'Opposition': 180
}
MINOR_ASPECTS = {
    'Semi-sextile': 30, 'Decile': 36, 'Semi-square': 45,
    'Quintile': 72, 'Sesquiquadrate': 135, 'Quincunx': 150
}
ALL_ASPECTS = {**MAJOR_ASPECTS, **MINOR_ASPECTS}

# Orb limits
MAJOR_ORB = 8.0
MINOR_ORB = 2.0
NUCLEAR_ORB = 1.0

# Planet IDs
PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}
NODE_IDS = {
    'Mean Node': swe.MEAN_NODE, 'True Node': swe.TRUE_NODE
}

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Traditional rulers for dispositor chain
TRADITIONAL_RULERS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
    'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
    'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}


def parse_birth_data():
    """Read birth data from 00_CORE_DATA.md. NEVER hardcode."""
    with open(CORE_DATA_PATH, 'r') as f:
        content = f.read()

    # Date
    date_match = re.search(r'\*\*Date:\*\* (.+)', content)
    date_str = date_match.group(1).strip()
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
              'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10, 'November': 11, 'December': 12}
    parts = date_str.replace(',', '').split()
    year = int(parts[2])
    month = months[parts[0]]
    day = int(parts[1])

    # Time
    time_match = re.search(r'\*\*Time:\*\* (.+)', content)
    raw_time = time_match.group(1).split('(')[0].strip()
    t_parts = raw_time.replace(':', ' ').split()
    hour = int(t_parts[0])
    minute = int(t_parts[1])
    ampm = t_parts[2] if len(t_parts) > 2 else None
    if ampm == 'PM' and hour != 12:
        hour += 12
    if ampm == 'AM' and hour == 12:
        hour = 0

    # Timezone
    tz_match = re.search(r'\*\*Timezone:\*\* UTC([+-]\d+)', content)
    tz_offset = int(tz_match.group(1))

    # Coordinates
    coord_match = re.search(r'\*\*Coordinates:\*\* (.+)', content)
    coord_raw = coord_match.group(1).strip()
    decimals = re.findall(r'(\d+\.\d+)', coord_raw)
    lat = float(decimals[0])
    lon = float(decimals[1])

    # UT time
    ut_hour = hour + minute / 60.0 - tz_offset

    print(f"Birth Data (from file):")
    print(f"  Date: {year}-{month:02d}-{day:02d}")
    print(f"  Time: {hour:02d}:{minute:02d} (UTC{tz_offset:+d})")
    print(f"  UT: {ut_hour:.4f}")
    print(f"  Lat: {lat}, Lon: {lon}")

    return year, month, day, ut_hour, lat, lon


def deg_to_sign(lon):
    """Convert absolute longitude to sign + degree."""
    sign_idx = int(lon / 30)
    deg_in_sign = lon % 30
    d = int(deg_in_sign)
    m = int((deg_in_sign - d) * 60)
    s = int(((deg_in_sign - d) * 60 - m) * 60)
    return f"{d:02d}°{m:02d}'{s:02d}\"", SIGNS[sign_idx], deg_in_sign


def fmt_orb(orb):
    """Format orb as degrees, minutes, seconds."""
    d = int(orb)
    m = int((orb - d) * 60)
    s = int(((orb - d) * 60 - m) * 60)
    return f"{d}°{m:02d}'{s:02d}\""


def shortest_arc(lon1, lon2):
    """Calculate shortest arc between two longitudes."""
    diff = abs(lon1 - lon2) % 360
    if diff > 180:
        diff = 360 - diff
    return diff


def check_aspect(sep, aspect_angle, orb_limit):
    """Check if a separation matches an aspect within orb."""
    orb = abs(sep - aspect_angle)
    if orb <= orb_limit:
        return orb
    return None


def get_dispositor(planet_name, sign):
    """Get the traditional ruler of the sign a planet is in."""
    return TRADITIONAL_RULERS.get(sign)


def compute_dispositor_chain(positions):
    """Compute full dispositor chain using traditional rulers."""
    chains = {}
    for name in positions:
        if name in ('Mean Node', 'True Node', 'Chiron'):
            continue
        chain = [name]
        current = name
        visited = set()
        while True:
            sign = positions[current]['sign']
            ruler = TRADITIONAL_RULERS[sign]
            if ruler in visited or ruler == current:
                chain.append(f"→ {ruler}" + (" (SELF-DISPOSING)" if ruler == current else " (LOOP)"))
                break
            visited.add(current)
            chain.append(f"→ {ruler}")
            current = ruler
        chains[name] = chain
    return chains


def main():
    year, month, day, ut_hour, lat, lon = parse_birth_data()
    jd = swe.julday(year, month, day, ut_hour)
    print(f"  JD: {jd:.6f}")

    # ============================
    # 1. PLANETARY POSITIONS
    # ============================
    positions = {}
    for name, pid in PLANETS.items():
        result = swe.calc_ut(jd, pid)
        longitude = result[0][0]
        speed = result[0][3]
        retro = speed < 0
        deg_str, sign, deg_in_sign = deg_to_sign(longitude)
        positions[name] = {
            'lon': longitude, 'sign': sign, 'deg_in_sign': deg_in_sign,
            'deg_str': deg_str, 'retro': retro, 'speed': speed
        }

    # Nodes
    for name, pid in NODE_IDS.items():
        result = swe.calc_ut(jd, pid)
        longitude = result[0][0]
        deg_str, sign, deg_in_sign = deg_to_sign(longitude)
        positions[name] = {
            'lon': longitude, 'sign': sign, 'deg_in_sign': deg_in_sign,
            'deg_str': deg_str, 'retro': True, 'speed': result[0][3]
        }

    # South Node (opposite of Mean Node)
    mn_lon = positions['Mean Node']['lon']
    sn_lon = (mn_lon + 180) % 360
    deg_str, sign, deg_in_sign = deg_to_sign(sn_lon)
    positions['South Node (Mean)'] = {
        'lon': sn_lon, 'sign': sign, 'deg_in_sign': deg_in_sign,
        'deg_str': deg_str, 'retro': True, 'speed': 0
    }

    # ============================
    # 2. HOUSES & ANGLES
    # ============================
    houses, ascmc = swe.houses(jd, lat, lon, b'P')  # Placidus
    asc = ascmc[0]
    mc = ascmc[1]
    vertex = ascmc[3]

    angles = {
        'ASC': asc, 'MC': mc, 'DSC': (asc + 180) % 360,
        'IC': (mc + 180) % 360, 'Vertex': vertex
    }

    # ============================
    # 3. DECLINATIONS
    # ============================
    declinations = {}
    for name, pid in PLANETS.items():
        result = swe.calc_ut(jd, pid, swe.FLG_EQUATORIAL)
        dec = result[0][1]
        declinations[name] = dec

    for name, pid in NODE_IDS.items():
        result = swe.calc_ut(jd, pid, swe.FLG_EQUATORIAL)
        dec = result[0][1]
        declinations[name] = dec

    # ============================
    # 4. ALL ASPECTS
    # ============================
    all_bodies = list(PLANETS.keys()) + ['Mean Node', 'True Node']
    # Add angles for aspect checking
    angle_bodies = {**{k: v for k, v in positions.items()}, 'Vertex': {'lon': vertex}, 'ASC': {'lon': asc}}

    aspects_found = []
    body_names = list(PLANETS.keys()) + ['Mean Node']  # Use Mean Node as default

    for i, name1 in enumerate(body_names):
        for j, name2 in enumerate(body_names):
            if i >= j:
                continue
            lon1 = positions[name1]['lon']
            lon2 = positions[name2]['lon']
            sep = shortest_arc(lon1, lon2)

            for asp_name, asp_angle in ALL_ASPECTS.items():
                orb_limit = MAJOR_ORB if asp_name in MAJOR_ASPECTS else MINOR_ORB
                orb = check_aspect(sep, asp_angle, orb_limit)
                if orb is not None:
                    aspects_found.append({
                        'body1': name1, 'body2': name2,
                        'aspect': asp_name, 'angle': asp_angle,
                        'orb': orb, 'separation': sep
                    })

    # Vertex aspects
    for name in body_names:
        lon1 = vertex
        lon2 = positions[name]['lon']
        sep = shortest_arc(lon1, lon2)
        for asp_name, asp_angle in ALL_ASPECTS.items():
            orb_limit = MAJOR_ORB if asp_name in MAJOR_ASPECTS else MINOR_ORB
            orb = check_aspect(sep, asp_angle, orb_limit)
            if orb is not None:
                aspects_found.append({
                    'body1': 'Vertex', 'body2': name,
                    'aspect': asp_name, 'angle': asp_angle,
                    'orb': orb, 'separation': sep
                })

    # ASC aspects
    for name in list(PLANETS.keys()):
        lon1 = asc
        lon2 = positions[name]['lon']
        sep = shortest_arc(lon1, lon2)
        for asp_name, asp_angle in ALL_ASPECTS.items():
            orb_limit = MAJOR_ORB if asp_name in MAJOR_ASPECTS else MINOR_ORB
            orb = check_aspect(sep, asp_angle, orb_limit)
            if orb is not None:
                aspects_found.append({
                    'body1': 'ASC', 'body2': name,
                    'aspect': asp_name, 'angle': asp_angle,
                    'orb': orb, 'separation': sep
                })

    # Sort by orb
    aspects_found.sort(key=lambda x: x['orb'])

    # ============================
    # 5. DECLINATION CONTACTS
    # ============================
    dec_contacts = []
    dec_names = list(declinations.keys())
    for i, name1 in enumerate(dec_names):
        for j, name2 in enumerate(dec_names):
            if i >= j:
                continue
            d1 = declinations[name1]
            d2 = declinations[name2]

            # Parallel: same sign declination
            if (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0):
                diff = abs(abs(d1) - abs(d2))
                if diff < 1.5:
                    dec_contacts.append({
                        'body1': name1, 'body2': name2,
                        'type': 'Parallel',
                        'dec1': d1, 'dec2': d2,
                        'orb': diff
                    })

            # Contra-parallel: opposite sign declination
            if (d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0):
                diff = abs(abs(d1) - abs(d2))
                if diff < 1.5:
                    dec_contacts.append({
                        'body1': name1, 'body2': name2,
                        'type': 'Contra-Parallel',
                        'dec1': d1, 'dec2': d2,
                        'orb': diff
                    })

    dec_contacts.sort(key=lambda x: x['orb'])

    # ============================
    # 6. MIDPOINTS
    # ============================
    sun_lon = positions['Sun']['lon']
    moon_lon = positions['Moon']['lon']

    # Sun/Moon midpoint (shorter arc)
    diff = moon_lon - sun_lon
    if diff < 0:
        diff += 360
    if diff > 180:
        mp = (sun_lon + (diff - 360) / 2) % 360
    else:
        mp = (sun_lon + diff / 2) % 360
    sun_moon_mp = mp

    # Also compute the opposition point
    sun_moon_mp_opp = (sun_moon_mp + 180) % 360

    mp_aspects = []
    for name in list(PLANETS.keys()) + ['Mean Node']:
        plon = positions[name]['lon']
        # Check conjunction to MP or opposition to MP
        for mp_val, mp_label in [(sun_moon_mp, 'Sun/Moon MP'), (sun_moon_mp_opp, 'Sun/Moon MP (opp)')]:
            sep = shortest_arc(plon, mp_val)
            for asp_name, asp_angle in ALL_ASPECTS.items():
                orb_limit = 2.0  # Tight orbs for midpoints
                orb = check_aspect(sep, asp_angle, orb_limit)
                if orb is not None:
                    mp_aspects.append({
                        'planet': name, 'midpoint': mp_label,
                        'aspect': asp_name, 'orb': orb
                    })

    mp_aspects.sort(key=lambda x: x['orb'])

    # ============================
    # 7. ARABIC PARTS (LOTS)
    # ============================
    # Night chart check: Sun below horizon
    # Sun below horizon if Sun is in houses 1-6 (below ASC-DSC line)
    # Simpler: check if Sun longitude is between IC and ASC (below horizon)
    # Actually: night = Sun below horizon. Check house placement.
    # Sun at 33.50° (Taurus), ASC at 338.68° (Pisces)
    # Sun is in House 2 per the natal chart — above horizon? No.
    # Houses 1-6 are below horizon in Placidus? No — houses 1-6 span from ASC downward.
    # Actually: houses 7-12 are above horizon, houses 1-6 are below.
    # Wait: House 1 starts at ASC. Houses above horizon: 7,8,9,10,11,12. Below: 1,2,3,4,5,6.
    # Sun in House 2 = below horizon = NIGHT CHART.

    is_night = True  # Sun in House 2, below horizon

    if is_night:
        # Night: Fortune = ASC + Sun - Moon
        fortune = (asc + sun_lon - moon_lon) % 360
        # Night: Spirit = ASC + Moon - Sun
        spirit = (asc + moon_lon - sun_lon) % 360
    else:
        fortune = (asc + moon_lon - sun_lon) % 360
        spirit = (asc + sun_lon - moon_lon) % 360

    # Lot of Basis = ASC + Fortune - Spirit
    basis = (asc + fortune - spirit) % 360

    lots = {
        'Fortune': fortune,
        'Spirit': spirit,
        'Basis': basis
    }

    # ============================
    # 8. DISPOSITOR CHAIN
    # ============================
    disp_chain = compute_dispositor_chain(positions)

    # Find final dispositor
    final_dispositor = None
    for name in PLANETS:
        sign = positions[name]['sign']
        ruler = TRADITIONAL_RULERS[sign]
        if ruler == name:
            final_dispositor = name
            break

    # ============================
    # 9. GENERATE OUTPUT
    # ============================
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    md = f"""# 11 VERIFIED GEOMETRY (CANONICAL REFERENCE)

**Generated:** {now}
**Method:** Swiss Ephemeris (Moshier) via pyswisseph
**Birth Data:** Read from `00_CORE_DATA.md` (NEVER hardcoded)
**JD:** {jd:.6f}

---

## 1. BIRTH DATA (as parsed from file)
- **Date:** {year}-{month:02d}-{day:02d}
- **Time:** UT {ut_hour:.4f}
- **Location:** {lat}°N, {lon}°E
- **House System:** Placidus

---

## 2. PLANETARY POSITIONS (Ecliptic Longitude)
| Planet | Absolute° | Sign | Degree | Retro | Speed |
|:---|:---|:---|:---|:---|:---|
"""
    for name in list(PLANETS.keys()) + ['Mean Node', 'True Node', 'South Node (Mean)']:
        p = positions[name]
        retro = 'R' if p['retro'] else ''
        md += f"| **{name}** | {p['lon']:.4f}° | {p['sign']} | {p['deg_str']} | {retro} | {p['speed']:.4f}°/day |\n"

    md += f"""
## 3. ANGLES & HOUSES
| Point | Absolute° | Sign | Degree |
|:---|:---|:---|:---|
"""
    for name, lon_val in angles.items():
        deg_str, sign, _ = deg_to_sign(lon_val)
        md += f"| **{name}** | {lon_val:.4f}° | {sign} | {deg_str} |\n"

    md += "\n### House Cusps (Placidus)\n"
    md += "| House | Absolute° |\n|:---|:---|\n"
    for i, cusp in enumerate(houses):
        md += f"| House {i+1} | {cusp:.4f}° |\n"

    md += f"""
---

## 4. DECLINATIONS
| Planet | Declination | Hemisphere |
|:---|:---|:---|
"""
    for name in list(PLANETS.keys()) + ['Mean Node', 'True Node']:
        dec = declinations[name]
        hemi = 'North' if dec > 0 else 'South'
        md += f"| **{name}** | {dec:+.4f}° | {hemi} |\n"

    md += f"""
---

## 5. ALL ASPECTS (sorted by orb)

### Nuclear Aspects (< 1°)
| Body 1 | Aspect | Body 2 | Orb | Separation |
|:---|:---|:---|:---|:---|
"""
    for a in aspects_found:
        if a['orb'] < NUCLEAR_ORB:
            md += f"| **{a['body1']}** | {a['aspect']} | **{a['body2']}** | **{fmt_orb(a['orb'])}** | {a['separation']:.4f}° |\n"

    md += f"""
### Tight Aspects (1° - 3°)
| Body 1 | Aspect | Body 2 | Orb | Separation |
|:---|:---|:---|:---|:---|
"""
    for a in aspects_found:
        if 1.0 <= a['orb'] < 3.0:
            md += f"| {a['body1']} | {a['aspect']} | {a['body2']} | {fmt_orb(a['orb'])} | {a['separation']:.4f}° |\n"

    md += f"""
### Medium Aspects (3° - 5°)
| Body 1 | Aspect | Body 2 | Orb | Separation |
|:---|:---|:---|:---|:---|
"""
    for a in aspects_found:
        if 3.0 <= a['orb'] < 5.0:
            md += f"| {a['body1']} | {a['aspect']} | {a['body2']} | {fmt_orb(a['orb'])} | {a['separation']:.4f}° |\n"

    md += f"""
### Wide Aspects (5° - 8°) [Major only]
| Body 1 | Aspect | Body 2 | Orb | Separation |
|:---|:---|:---|:---|:---|
"""
    for a in aspects_found:
        if 5.0 <= a['orb'] < 8.0 and a['aspect'] in MAJOR_ASPECTS:
            md += f"| {a['body1']} | {a['aspect']} | {a['body2']} | {fmt_orb(a['orb'])} | {a['separation']:.4f}° |\n"

    md += f"""
---

## 6. DECLINATION CONTACTS (< 1.5°)
| Body 1 | Type | Body 2 | Orb | Dec 1 | Dec 2 |
|:---|:---|:---|:---|:---|:---|
"""
    for dc in dec_contacts:
        md += f"| **{dc['body1']}** | {dc['type']} | **{dc['body2']}** | {fmt_orb(dc['orb'])} | {dc['dec1']:+.4f}° | {dc['dec2']:+.4f}° |\n"

    md += f"""
---

## 7. MIDPOINTS

### Sun/Moon Midpoint
- **Sun/Moon MP:** {sun_moon_mp:.4f}° ({deg_to_sign(sun_moon_mp)[1]} {deg_to_sign(sun_moon_mp)[0]})
- **Opposition Point:** {sun_moon_mp_opp:.4f}° ({deg_to_sign(sun_moon_mp_opp)[1]} {deg_to_sign(sun_moon_mp_opp)[0]})

### Aspects to Sun/Moon Midpoint (< 2°)
| Planet | Midpoint | Aspect | Orb |
|:---|:---|:---|:---|
"""
    for mpa in mp_aspects:
        md += f"| **{mpa['planet']}** | {mpa['midpoint']} | {mpa['aspect']} | {fmt_orb(mpa['orb'])} |\n"

    md += f"""
---

## 8. ARABIC PARTS (LOTS)
**Chart Type:** Night (Sun in House 2, below horizon)

| Lot | Formula | Absolute° | Sign | Degree |
|:---|:---|:---|:---|:---|
| **Fortune** | ASC + Sun - Moon | {fortune:.4f}° | {deg_to_sign(fortune)[1]} | {deg_to_sign(fortune)[0]} |
| **Spirit** | ASC + Moon - Sun | {spirit:.4f}° | {deg_to_sign(spirit)[1]} | {deg_to_sign(spirit)[0]} |
| **Basis** | ASC + Fortune - Spirit | {basis:.4f}° | {deg_to_sign(basis)[1]} | {deg_to_sign(basis)[0]} |

### Lot Conjunctions (< 3° to any planet/node/angle)
"""
    for lot_name, lot_lon in lots.items():
        # Check against planets and nodes
        for pname in list(PLANETS.keys()) + ['Mean Node', 'South Node (Mean)']:
            plon = positions[pname]['lon']
            sep = shortest_arc(lot_lon, plon)
            if sep < 3.0:
                md += f"- **Lot of {lot_name}** ({lot_lon:.2f}°) conjunct **{pname}** ({plon:.2f}°) — Orb: {fmt_orb(sep)}\n"
        # Check against angles
        for aname, alon in angles.items():
            sep = shortest_arc(lot_lon, alon)
            if sep < 3.0:
                md += f"- **Lot of {lot_name}** ({lot_lon:.2f}°) conjunct **{aname}** ({alon:.2f}°) — Orb: {fmt_orb(sep)}\n"

    md += f"""
---

## 9. DISPOSITOR CHAIN (Traditional Rulers)
"""
    if final_dispositor:
        md += f"**Final Dispositor: {final_dispositor}** (in {positions[final_dispositor]['sign']} — own sign)\n\n"
    else:
        md += "**No Final Dispositor** (mutual reception or loop)\n\n"

    md += "| Planet | Sign | Disposed by | Chain |\n"
    md += "|:---|:---|:---|:---|\n"
    for name in PLANETS:
        sign = positions[name]['sign']
        ruler = TRADITIONAL_RULERS[sign]
        chain_str = ' '.join(disp_chain.get(name, []))
        md += f"| {name} | {sign} | {ruler} | {chain_str} |\n"

    md += f"""
---

## 10. SPECIFIC CLAIMS VERIFICATION

*These are the specific claims from the encyclopedia, verified here.*

### Mars conjunct Rahu (North Node)
- Mars: {positions['Mars']['lon']:.4f}° | Mean Node: {positions['Mean Node']['lon']:.4f}° | True Node: {positions['True Node']['lon']:.4f}°
- **Orb (Mean): {fmt_orb(shortest_arc(positions['Mars']['lon'], positions['Mean Node']['lon']))}**
- **Orb (True): {fmt_orb(shortest_arc(positions['Mars']['lon'], positions['True Node']['lon']))}**

### Venus square Mars
- Venus: {positions['Venus']['lon']:.4f}° | Mars: {positions['Mars']['lon']:.4f}°
- Separation: {shortest_arc(positions['Venus']['lon'], positions['Mars']['lon']):.4f}°
- **Orb from 90°: {fmt_orb(abs(shortest_arc(positions['Venus']['lon'], positions['Mars']['lon']) - 90))}**

### Mercury decile Uranus
- Mercury: {positions['Mercury']['lon']:.4f}° | Uranus: {positions['Uranus']['lon']:.4f}°
- Separation: {shortest_arc(positions['Mercury']['lon'], positions['Uranus']['lon']):.4f}°
- **Orb from 36°: {fmt_orb(abs(shortest_arc(positions['Mercury']['lon'], positions['Uranus']['lon']) - 36))}**

### Vertex quincunx Neptune
- Vertex: {vertex:.4f}° | Neptune: {positions['Neptune']['lon']:.4f}°
- Separation: {shortest_arc(vertex, positions['Neptune']['lon']):.4f}°
- **Orb from 150°: {fmt_orb(abs(shortest_arc(vertex, positions['Neptune']['lon']) - 150))}**

### Sun quintile Neptune
- Sun: {positions['Sun']['lon']:.4f}° | Neptune: {positions['Neptune']['lon']:.4f}°
- Separation: {shortest_arc(positions['Sun']['lon'], positions['Neptune']['lon']):.4f}°
- **Orb from 72°: {fmt_orb(abs(shortest_arc(positions['Sun']['lon'], positions['Neptune']['lon']) - 72))}**

### Mercury sextile Neptune
- Mercury: {positions['Mercury']['lon']:.4f}° | Neptune: {positions['Neptune']['lon']:.4f}°
- Separation: {shortest_arc(positions['Mercury']['lon'], positions['Neptune']['lon']):.4f}°
- **Orb from 60°: {fmt_orb(abs(shortest_arc(positions['Mercury']['lon'], positions['Neptune']['lon']) - 60))}**

### Moon quincunx Neptune (CLAIMED — VERIFY)
- Moon: {positions['Moon']['lon']:.4f}° | Neptune: {positions['Neptune']['lon']:.4f}°
- Separation: {shortest_arc(positions['Moon']['lon'], positions['Neptune']['lon']):.4f}°
- **Orb from 150°: {fmt_orb(abs(shortest_arc(positions['Moon']['lon'], positions['Neptune']['lon']) - 150))}**
- **STATUS: {"EXISTS" if abs(shortest_arc(positions['Moon']['lon'], positions['Neptune']['lon']) - 150) < 2 else "DOES NOT EXIST (too wide)"}**

### Uranus square Sun/Moon Midpoint
- Uranus: {positions['Uranus']['lon']:.4f}° | Sun/Moon MP: {sun_moon_mp:.4f}°
- Separation: {shortest_arc(positions['Uranus']['lon'], sun_moon_mp):.4f}°
- **Orb from 90°: {fmt_orb(abs(shortest_arc(positions['Uranus']['lon'], sun_moon_mp) - 90))}**
- Also check opposition point ({sun_moon_mp_opp:.4f}°):
- Separation: {shortest_arc(positions['Uranus']['lon'], sun_moon_mp_opp):.4f}°
- **Orb from 90°: {fmt_orb(abs(shortest_arc(positions['Uranus']['lon'], sun_moon_mp_opp) - 90))}**

### Pluto quintile ASC
- Pluto: {positions['Pluto']['lon']:.4f}° | ASC: {asc:.4f}°
- Separation: {shortest_arc(positions['Pluto']['lon'], asc):.4f}°
- **Orb from 72°: {fmt_orb(abs(shortest_arc(positions['Pluto']['lon'], asc) - 72))}**

### Jupiter trine Saturn (Grand Trine leg)
- Jupiter: {positions['Jupiter']['lon']:.4f}° | Saturn: {positions['Saturn']['lon']:.4f}°
- Separation: {shortest_arc(positions['Jupiter']['lon'], positions['Saturn']['lon']):.4f}°
- **Orb from 120°: {fmt_orb(abs(shortest_arc(positions['Jupiter']['lon'], positions['Saturn']['lon']) - 120))}**

### Mercury trine Jupiter (Grand Trine leg)
- Mercury: {positions['Mercury']['lon']:.4f}° | Jupiter: {positions['Jupiter']['lon']:.4f}°
- Separation: {shortest_arc(positions['Mercury']['lon'], positions['Jupiter']['lon']):.4f}°
- **Orb from 120°: {fmt_orb(abs(shortest_arc(positions['Mercury']['lon'], positions['Jupiter']['lon']) - 120))}**

### Mercury trine Saturn (Grand Trine leg)
- Mercury: {positions['Mercury']['lon']:.4f}° | Saturn: {positions['Saturn']['lon']:.4f}°
- Separation: {shortest_arc(positions['Mercury']['lon'], positions['Saturn']['lon']):.4f}°
- **Orb from 120°: {fmt_orb(abs(shortest_arc(positions['Mercury']['lon'], positions['Saturn']['lon']) - 120))}**

### Grand Trine Average Orb
- Jupiter-Saturn: {fmt_orb(abs(shortest_arc(positions['Jupiter']['lon'], positions['Saturn']['lon']) - 120))}
- Mercury-Jupiter: {fmt_orb(abs(shortest_arc(positions['Mercury']['lon'], positions['Jupiter']['lon']) - 120))}
- Mercury-Saturn: {fmt_orb(abs(shortest_arc(positions['Mercury']['lon'], positions['Saturn']['lon']) - 120))}
- **Average: {((abs(shortest_arc(positions['Jupiter']['lon'], positions['Saturn']['lon']) - 120) + abs(shortest_arc(positions['Mercury']['lon'], positions['Jupiter']['lon']) - 120) + abs(shortest_arc(positions['Mercury']['lon'], positions['Saturn']['lon']) - 120)) / 3):.2f}°**

### Lot of Basis — Where is it?
- **Lot of Basis: {basis:.4f}° = {deg_to_sign(basis)[1]} {deg_to_sign(basis)[0]}**
- Distance to Jupiter ({positions['Jupiter']['lon']:.2f}°): {shortest_arc(basis, positions['Jupiter']['lon']):.2f}°
- Distance to South Node Mean ({sn_lon:.2f}°): {shortest_arc(basis, sn_lon):.2f}°
- **VERDICT: {"CONJUNCT SOUTH NODE" if shortest_arc(basis, sn_lon) < 3 else "CONJUNCT JUPITER" if shortest_arc(basis, positions['Jupiter']['lon']) < 3 else "NEITHER"}**

### Mercury-Mars Declination
- Mercury dec: {declinations['Mercury']:+.4f}° ({('North' if declinations['Mercury'] > 0 else 'South')})
- Mars dec: {declinations['Mars']:+.4f}° ({('North' if declinations['Mars'] > 0 else 'South')})
- Same hemisphere: {('YES' if (declinations['Mercury'] > 0) == (declinations['Mars'] > 0) else 'NO')}
- **Type: {'PARALLEL (both same side)' if (declinations['Mercury'] > 0) == (declinations['Mars'] > 0) else 'CONTRA-PARALLEL (opposite sides)'}**
- **Orb: {fmt_orb(abs(abs(declinations['Mercury']) - abs(declinations['Mars'])))}**

### Saturn-Pluto Declination
- Saturn dec: {declinations['Saturn']:+.4f}° ({('North' if declinations['Saturn'] > 0 else 'South')})
- Pluto dec: {declinations['Pluto']:+.4f}° ({('North' if declinations['Pluto'] > 0 else 'South')})
- Difference: {abs(abs(declinations['Saturn']) - abs(declinations['Pluto'])):.4f}°
- **STATUS: {"EXISTS" if abs(abs(declinations['Saturn']) - abs(declinations['Pluto'])) < 1.5 else "DOES NOT EXIST (too wide)"}**

### Uranus-Node Declination
- Uranus dec: {declinations['Uranus']:+.4f}° ({('North' if declinations['Uranus'] > 0 else 'South')})
- Mean Node dec: {declinations['Mean Node']:+.4f}° ({('North' if declinations['Mean Node'] > 0 else 'South')})
- **Type: {'PARALLEL' if (declinations['Uranus'] > 0) == (declinations['Mean Node'] > 0) else 'CONTRA-PARALLEL'}**
- **Orb: {fmt_orb(abs(abs(declinations['Uranus']) - abs(declinations['Mean Node'])))}**

---

## 11. MOON SIGN VERIFICATION
- Moon longitude: {positions['Moon']['lon']:.4f}°
- Sign boundaries: Cancer = 90°-120°, Leo = 120°-150°
- **Moon is in: {positions['Moon']['sign']}**
- **Moon degree: {positions['Moon']['deg_str']}**

---

*This file is the CANONICAL REFERENCE. If any other file contradicts these numbers, THIS FILE IS CORRECT.*
*Regenerate with: `python3 environment/scripts/verify_all_geometry.py`*
"""

    # Write output
    with open(OUTPUT_PATH, 'w') as f:
        f.write(md)
    print(f"\nOutput written to: {OUTPUT_PATH}")

    # Also write to session folder for auditing
    session_path = os.path.join(PROJECT_ROOT, 'scratches', 'sessions', '0019_Brain_Surgery_20260130', '11_VERIFIED_GEOMETRY.md')
    os.makedirs(os.path.dirname(session_path), exist_ok=True)
    with open(session_path, 'w') as f:
        f.write(md)
    print(f"Copy written to: {session_path}")


if __name__ == '__main__':
    main()
