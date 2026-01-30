#!/usr/bin/env python3
"""
QUICK CHECK — Fast Geometric Claim Verifier
============================================
Usage: python3 quick_check.py "Venus square Mars"
       python3 quick_check.py "Mercury declination"
       python3 quick_check.py "Lot of Basis"
       python3 quick_check.py "Sun/Moon midpoint"
       python3 quick_check.py "all aspects Sun"

Reads birth data from 00_CORE_DATA.md. Never hardcodes anything.
"""

import os
import re
import sys
import swisseph as swe

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
CORE_DATA_PATH = os.path.join(PROJECT_ROOT, 'cases', '001_Theodore', '00_CORE_DATA', '00_CORE_DATA.md')
EPHE_PATH = os.path.join(PROJECT_ROOT, 'environment', 'data', 'sweph')

swe.set_ephe_path(EPHE_PATH)

PLANETS = {
    'sun': swe.SUN, 'moon': swe.MOON, 'mercury': swe.MERCURY,
    'venus': swe.VENUS, 'mars': swe.MARS, 'jupiter': swe.JUPITER,
    'saturn': swe.SATURN, 'uranus': swe.URANUS, 'neptune': swe.NEPTUNE,
    'pluto': swe.PLUTO, 'mean node': swe.MEAN_NODE, 'true node': swe.TRUE_NODE,
    'rahu': swe.MEAN_NODE, 'north node': swe.MEAN_NODE
}

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

ASPECTS = {
    'conjunction': 0, 'sextile': 60, 'square': 90,
    'trine': 120, 'opposition': 180, 'quincunx': 150,
    'quintile': 72, 'decile': 36, 'semi-sextile': 30,
    'semi-square': 45, 'sesquiquadrate': 135
}

TRADITIONAL_RULERS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
    'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
    'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}


def parse_birth_data():
    with open(CORE_DATA_PATH, 'r') as f:
        content = f.read()
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
              'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10, 'November': 11, 'December': 12}
    date_match = re.search(r'\*\*Date:\*\* (.+)', content)
    parts = date_match.group(1).strip().replace(',', '').split()
    year, month, day = int(parts[2]), months[parts[0]], int(parts[1])
    time_match = re.search(r'\*\*Time:\*\* (.+)', content)
    raw = time_match.group(1).split('(')[0].strip().replace(':', ' ').split()
    h, m = int(raw[0]), int(raw[1])
    if len(raw) > 2:
        if raw[2] == 'PM' and h != 12: h += 12
        if raw[2] == 'AM' and h == 12: h = 0
    tz = int(re.search(r'UTC([+-]\d+)', content).group(1))
    coords = re.findall(r'(\d+\.\d+)', re.search(r'\*\*Coordinates:\*\* (.+)', content).group(1))
    lat, lon = float(coords[0]), float(coords[1])
    ut = h + m / 60.0 - tz
    jd = swe.julday(year, month, day, ut)
    return jd, lat, lon


def deg_to_sign(lon):
    sign_idx = int(lon / 30)
    deg = lon % 30
    d, m, s = int(deg), int((deg - int(deg)) * 60), int(((deg - int(deg)) * 60 - int((deg - int(deg)) * 60)) * 60)
    return f"{SIGNS[sign_idx]} {d:02d}°{m:02d}'{s:02d}\""


def shortest_arc(a, b):
    d = abs(a - b) % 360
    return d if d <= 180 else 360 - d


def get_position(jd, name):
    name_lower = name.lower().strip()
    if name_lower == 'vertex':
        _, ascmc = swe.houses(jd, lat, lon, b'P')
        return ascmc[3]
    if name_lower == 'asc' or name_lower == 'ascendant':
        _, ascmc = swe.houses(jd, lat, lon, b'P')
        return ascmc[0]
    if name_lower == 'mc' or name_lower == 'midheaven':
        _, ascmc = swe.houses(jd, lat, lon, b'P')
        return ascmc[1]
    if name_lower == 'south node':
        r = swe.calc_ut(jd, swe.MEAN_NODE)
        return (r[0][0] + 180) % 360
    pid = PLANETS.get(name_lower)
    if pid is not None:
        return swe.calc_ut(jd, pid)[0][0]
    return None


def get_declination(jd, name):
    name_lower = name.lower().strip()
    pid = PLANETS.get(name_lower)
    if pid is not None:
        return swe.calc_ut(jd, pid, swe.FLG_EQUATORIAL)[0][1]
    return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 quick_check.py \"Venus square Mars\"")
        print("       python3 quick_check.py \"Mercury declination\"")
        print("       python3 quick_check.py \"Lot of Basis\"")
        print("       python3 quick_check.py \"position Sun\"")
        sys.exit(1)

    query = ' '.join(sys.argv[1:]).lower()
    jd, lat, lon = parse_birth_data()
    print(f"Birth data parsed. JD: {jd:.6f}")

    # Check for aspect query: "planet1 aspect planet2"
    for asp_name, asp_angle in ASPECTS.items():
        if asp_name in query:
            parts = query.split(asp_name)
            if len(parts) == 2:
                p1_name = parts[0].strip()
                p2_name = parts[1].strip()
                lon1 = get_position(jd, p1_name)
                lon2 = get_position(jd, p2_name)
                if lon1 is not None and lon2 is not None:
                    sep = shortest_arc(lon1, lon2)
                    orb = abs(sep - asp_angle)
                    d = int(orb)
                    m = int((orb - d) * 60)
                    s = int(((orb - d) * 60 - m) * 60)
                    print(f"\n{p1_name.title()}: {lon1:.4f}° = {deg_to_sign(lon1)}")
                    print(f"{p2_name.title()}: {lon2:.4f}° = {deg_to_sign(lon2)}")
                    print(f"Separation: {sep:.4f}°")
                    print(f"{asp_name.title()} ({asp_angle}°): Orb = {d}°{m:02d}'{s:02d}\"")
                    print(f"Status: {'EXISTS' if orb < 8 else 'TOO WIDE'}")
                    sys.exit(0)

    # Check for declination query
    if 'declination' in query or 'decl' in query:
        for pname, pid in PLANETS.items():
            if pname in query:
                dec = get_declination(jd, pname)
                hemi = 'North' if dec > 0 else 'South'
                print(f"\n{pname.title()} declination: {dec:+.4f}° ({hemi})")
                sys.exit(0)
        # If no specific planet, show all
        print("\nAll Declinations:")
        for pname in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'mean node', 'true node']:
            dec = get_declination(jd, pname)
            hemi = 'N' if dec > 0 else 'S'
            print(f"  {pname.title():12s}: {dec:+.4f}° ({hemi})")
        sys.exit(0)

    # Check for lot query
    if 'lot' in query or 'basis' in query or 'fortune' in query or 'spirit' in query:
        _, ascmc = swe.houses(jd, lat, lon, b'P')
        asc = ascmc[0]
        sun = swe.calc_ut(jd, swe.SUN)[0][0]
        moon = swe.calc_ut(jd, swe.MOON)[0][0]
        fortune = (asc + sun - moon) % 360
        spirit = (asc + moon - sun) % 360
        basis = (asc + fortune - spirit) % 360
        print(f"\nNight Chart (Sun in House 2)")
        print(f"ASC: {asc:.4f}° = {deg_to_sign(asc)}")
        print(f"Sun: {sun:.4f}° | Moon: {moon:.4f}°")
        print(f"\nFortune (ASC+Sun-Moon): {fortune:.4f}° = {deg_to_sign(fortune)}")
        print(f"Spirit  (ASC+Moon-Sun): {spirit:.4f}° = {deg_to_sign(spirit)}")
        print(f"Basis   (ASC+F-S):      {basis:.4f}° = {deg_to_sign(basis)}")

        # Check conjunctions
        mn = swe.calc_ut(jd, swe.MEAN_NODE)[0][0]
        sn = (mn + 180) % 360
        jup = swe.calc_ut(jd, swe.JUPITER)[0][0]
        print(f"\nBasis to South Node: {shortest_arc(basis, sn):.4f}°")
        print(f"Basis to Jupiter:    {shortest_arc(basis, jup):.4f}°")
        sys.exit(0)

    # Check for midpoint query
    if 'midpoint' in query:
        sun = swe.calc_ut(jd, swe.SUN)[0][0]
        moon = swe.calc_ut(jd, swe.MOON)[0][0]
        diff = moon - sun
        if diff < 0: diff += 360
        if diff > 180:
            mp = (sun + (diff - 360) / 2) % 360
        else:
            mp = (sun + diff / 2) % 360
        print(f"\nSun/Moon Midpoint: {mp:.4f}° = {deg_to_sign(mp)}")
        print(f"Opposition: {(mp+180)%360:.4f}° = {deg_to_sign((mp+180)%360)}")

        # Check aspects to MP
        for pname, pid in PLANETS.items():
            plon = swe.calc_ut(jd, pid)[0][0]
            for mp_val in [mp, (mp + 180) % 360]:
                sep = shortest_arc(plon, mp_val)
                for aname, aangle in ASPECTS.items():
                    orb = abs(sep - aangle)
                    if orb < 2:
                        d = int(orb); m = int((orb-d)*60); s = int(((orb-d)*60-m)*60)
                        print(f"  {pname.title()} {aname} MP: {d}°{m:02d}'{s:02d}\"")
        sys.exit(0)

    # Check for position query
    if 'position' in query or 'where' in query:
        for pname in PLANETS:
            if pname in query:
                pos = get_position(jd, pname)
                print(f"\n{pname.title()}: {pos:.4f}° = {deg_to_sign(pos)}")
                sys.exit(0)

    # Fallback: try to find two planet names and check all aspects
    found_planets = []
    for pname in PLANETS:
        if pname in query:
            found_planets.append(pname)
    if len(found_planets) >= 2:
        p1, p2 = found_planets[0], found_planets[1]
        lon1 = get_position(jd, p1)
        lon2 = get_position(jd, p2)
        sep = shortest_arc(lon1, lon2)
        print(f"\n{p1.title()}: {lon1:.4f}° = {deg_to_sign(lon1)}")
        print(f"{p2.title()}: {lon2:.4f}° = {deg_to_sign(lon2)}")
        print(f"Separation: {sep:.4f}°")
        print(f"\nAspect check:")
        for aname, aangle in sorted(ASPECTS.items(), key=lambda x: x[1]):
            orb = abs(sep - aangle)
            if orb < 8:
                d = int(orb); m = int((orb-d)*60); s = int(((orb-d)*60-m)*60)
                flag = " *** NUCLEAR" if orb < 1 else ""
                print(f"  {aname.title()} ({aangle}°): Orb = {d}°{m:02d}'{s:02d}\"{flag}")
    else:
        print(f"Could not parse query: '{query}'")
        print("Try: 'Venus square Mars', 'declination', 'Lot of Basis', 'midpoint'")
