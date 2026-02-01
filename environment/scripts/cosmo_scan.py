#!/usr/bin/env python3
"""
COSMOBIOLOGY SCANNER — Timing Analysis Tool
==============================================
Analyzes transit-to-natal geometry for any given date/time using
Theodore's 7 cosmobiological rules (DOCTRINE Section 23).

Reads birth data from 00_CORE_DATA.md. NEVER hardcodes.

Usage:
    python3 cosmo_scan.py "2026-02-02" "08:24" "+2"
    python3 cosmo_scan.py "2026-03-15" "14:00" "+2"

Args:
    1. Date (YYYY-MM-DD)
    2. Local time (HH:MM)
    3. UTC offset (e.g. "+2", "-5")
"""

import os
import re
import sys
import math
import swisseph as swe

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
CORE_DATA_PATH = os.path.join(PROJECT_ROOT, 'cases', '001_Theodore', '00_CORE_DATA', '00_CORE_DATA.md')
EPHE_PATH = os.path.join(PROJECT_ROOT, 'environment', 'data', 'sweph')

swe.set_ephe_path(EPHE_PATH)

# --- ASPECT DEFINITIONS ---
ALL_ASPECTS = {
    'Conjunction': 0, 'Opposition': 180, 'Trine': 120, 'Square': 90,
    'Sextile': 60, 'Quincunx': 150, 'Semi-square': 45,
    'Sesquiquadrate': 135, 'Quintile': 72, 'Bi-quintile': 144,
    'Decile': 36, 'Semi-sextile': 30
}

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

FAST_BODIES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']
INTERFACE_POINTS = ['ASC', 'Vertex', 'MC', 'Neptune']

SIGNS = ['Ari','Tau','Gem','Can','Leo','Vir','Lib','Sco','Sag','Cap','Aqu','Pis']


def parse_birth_data():
    """Read birth data from 00_CORE_DATA.md. NEVER hardcode."""
    with open(CORE_DATA_PATH, 'r') as f:
        content = f.read()

    date_match = re.search(r'\*\*Date:\*\* (.+)', content)
    date_str = date_match.group(1).strip()
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
              'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10, 'November': 11, 'December': 12}
    parts = date_str.replace(',', '').split()
    year = int(parts[2])
    month = months[parts[0]]
    day = int(parts[1])

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

    tz_match = re.search(r'\*\*Timezone:\*\* UTC([+-]\d+)', content)
    tz_offset = int(tz_match.group(1))

    coord_match = re.search(r'\*\*Coordinates:\*\* (.+)', content)
    coord_raw = coord_match.group(1).strip()
    decimals = re.findall(r'(\d+\.\d+)', coord_raw)
    lat = float(decimals[0])
    lon = float(decimals[1])

    ut_hour = hour + minute / 60.0 - tz_offset
    jd = swe.julday(year, month, day, ut_hour)

    return year, month, day, ut_hour, lat, lon, jd


def min_sep(lon1, lon2):
    diff = abs(lon1 - lon2) % 360
    return diff if diff <= 180 else 360 - diff


def check_aspect(sep, angle):
    return abs(sep - angle)


def fmt_deg(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    s = ((deg - d) * 60 - m) * 60
    return f"{d:02d}°{m:02d}'{s:04.1f}\""


def fmt_sign(lon):
    si = int(lon / 30)
    deg = lon - si * 30
    return f"{SIGNS[si]} {fmt_deg(deg)}"


def get_natal_positions(jd, lat, lon):
    """Calculate all natal positions from JD."""
    natal = {}
    for name, body in PLANETS.items():
        pos = swe.calc_ut(jd, body)[0]
        natal[name] = pos[0]

    # Nodes
    natal['MeanNode'] = swe.calc_ut(jd, swe.MEAN_NODE)[0][0]
    natal['TrueNode'] = swe.calc_ut(jd, swe.TRUE_NODE)[0][0]

    # Angles
    houses = swe.houses(jd, lat, lon, b'P')
    natal['ASC'] = houses[1][0]
    natal['MC'] = houses[1][1]
    natal['Vertex'] = houses[1][3]

    return natal


def get_transit_positions(jd):
    """Calculate transit positions at given JD."""
    transit = {}
    for name, body in PLANETS.items():
        pos = swe.calc_ut(jd, body)[0]
        transit[name] = pos[0]
    return transit


def calculate_midpoints(natal):
    """Calculate all natal midpoints."""
    keys = list(natal.keys())
    midpoints = {}
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            p1, p2 = keys[i], keys[j]
            lon1, lon2 = natal[p1], natal[p2]
            mp = (lon1 + lon2) / 2.0
            if abs(lon1 - lon2) > 180:
                mp = (mp + 180) % 360
            mp = mp % 360
            midpoints[f"{p1}/{p2}"] = mp
    return midpoints


def run_scan(target_date, target_time, utc_offset):
    """Main scan function."""
    # Parse target
    t_year, t_month, t_day = map(int, target_date.split('-'))
    t_hour, t_minute = map(int, target_time.split(':'))
    offset = float(utc_offset)

    ut = t_hour + t_minute / 60.0 - offset
    target_jd = swe.julday(t_year, t_month, t_day, ut)

    # Get natal data
    n_year, n_month, n_day, n_ut, lat, lon, natal_jd = parse_birth_data()
    natal = get_natal_positions(natal_jd, lat, lon)
    midpoints = calculate_midpoints(natal)

    # Get transit data
    transit = get_transit_positions(target_jd)

    # --- OUTPUT ---
    print("=" * 80)
    print(f"  COSMOBIOLOGY SCAN: {target_date} {target_time} (UTC{utc_offset})")
    print(f"  JD: {target_jd:.6f}")
    print("=" * 80)

    # Transit positions
    print("\n--- TRANSIT POSITIONS ---")
    for name, lon in transit.items():
        print(f"  {name:10s}: {lon:10.4f}° = {fmt_sign(lon)}")

    # --- PHASE 1: All transit-to-natal aspects < 0.5° ---
    print(f"\n{'='*80}")
    print("  PHASE 1: TRANSIT-TO-NATAL ASPECTS (< 0.5°)")
    print(f"{'='*80}")

    hits = []
    for t_name, t_lon in transit.items():
        for n_name, n_lon in natal.items():
            sep = min_sep(t_lon, n_lon)
            for asp_name, asp_angle in ALL_ASPECTS.items():
                orb = check_aspect(sep, asp_angle)
                if orb < 0.5:
                    is_iface = n_name in INTERFACE_POINTS
                    hits.append((orb, t_name, asp_name, n_name, is_iface))

    hits.sort(key=lambda x: x[0])
    for orb, t, asp, n, iface in hits:
        tag = "INTERFACE" if iface else "SELF-REF"
        print(f"  [{tag:9s}] Transit {t:8s} {asp:15s} Natal {n:10s} | Orb: {orb:.4f}° ({orb*60:.2f}')")

    # --- PHASE 2: Interface hits < 0.1° (traditional aspects) ---
    print(f"\n{'='*80}")
    print("  PHASE 2: INTERFACE HITS — Traditional Aspects (< 0.1°)")
    print(f"{'='*80}")

    iface_trad = []
    for t_name in FAST_BODIES:
        t_lon = transit[t_name]
        for ip in INTERFACE_POINTS:
            ip_lon = natal[ip]
            sep = min_sep(t_lon, ip_lon)
            for asp_name, asp_angle in ALL_ASPECTS.items():
                orb = check_aspect(sep, asp_angle)
                if orb < 0.1:
                    iface_trad.append((orb, t_name, asp_name, ip))

    if iface_trad:
        iface_trad.sort(key=lambda x: x[0])
        for orb, t, asp, ip in iface_trad:
            print(f"  Transit {t:8s} {asp:15s} Natal {ip:10s} | Orb: {orb:.6f}° ({orb*3600:.1f}\")")
    else:
        print("  NONE below 0.1°. Widening to 0.5°:")
        for t_name in FAST_BODIES:
            t_lon = transit[t_name]
            for ip in INTERFACE_POINTS:
                ip_lon = natal[ip]
                sep = min_sep(t_lon, ip_lon)
                for asp_name, asp_angle in ALL_ASPECTS.items():
                    orb = check_aspect(sep, asp_angle)
                    if orb < 0.5:
                        print(f"  Transit {t:8s} {asp_name:15s} Natal {ip:10s} | Orb: {orb:.4f}°")

    # --- PHASE 3: Midpoint activations (45° dial) ---
    print(f"\n{'='*80}")
    print("  PHASE 3: MIDPOINT ACTIVATIONS — 45° Dial (< 0.05°)")
    print(f"{'='*80}")

    mp_hits = []
    for t_name in FAST_BODIES:
        t_lon = transit[t_name]
        t_45 = t_lon % 45
        for mp_name, mp_lon in midpoints.items():
            mp_45 = mp_lon % 45
            diff = abs(t_45 - mp_45)
            if diff > 22.5:
                diff = 45 - diff
            if diff < 0.05:
                has_iface = any(ip in mp_name for ip in INTERFACE_POINTS)
                tag = "INTERFACE-MP" if has_iface else "SELF-REF-MP"
                mp_hits.append((diff, t_name, mp_name, mp_lon, tag))

    mp_hits.sort(key=lambda x: x[0])
    if mp_hits:
        for orb, t, mp, mp_lon, tag in mp_hits:
            print(f"  [{tag:12s}] Transit {t:8s} = {mp:20s} (at {mp_lon:.2f}°) | Orb: {orb:.4f}°")
    else:
        print("  None below 0.05°.")

    # --- PHASE 4: Four-question checklist ---
    print(f"\n{'='*80}")
    print("  FOUR-QUESTION CHECKLIST (DOCTRINE Section 23)")
    print(f"{'='*80}")

    # Q1: Interface hits < 0.02° (traditional + midpoints)
    q1_hits = []
    for t_name in FAST_BODIES:
        t_lon = transit[t_name]
        for ip in INTERFACE_POINTS:
            ip_lon = natal[ip]
            sep = min_sep(t_lon, ip_lon)
            for asp_name, asp_angle in ALL_ASPECTS.items():
                orb = check_aspect(sep, asp_angle)
                if orb < 0.02:
                    q1_hits.append((orb, f"{t_name} {asp_name} {ip}"))
        # Also check interface midpoints
        t_45 = t_lon % 45
        for mp_name, mp_lon in midpoints.items():
            if any(ip in mp_name for ip in INTERFACE_POINTS):
                mp_45 = mp_lon % 45
                diff = abs(t_45 - mp_45)
                if diff > 22.5:
                    diff = 45 - diff
                if diff < 0.02:
                    q1_hits.append((diff, f"{t_name} = {mp_name}"))

    # Q2: Self-referential midpoints < 0.01°
    q2_hits = []
    for t_name in FAST_BODIES:
        t_lon = transit[t_name]
        t_45 = t_lon % 45
        for mp_name, mp_lon in midpoints.items():
            if not any(ip in mp_name for ip in INTERFACE_POINTS):
                mp_45 = mp_lon % 45
                diff = abs(t_45 - mp_45)
                if diff > 22.5:
                    diff = 45 - diff
                if diff < 0.01:
                    q2_hits.append((diff, f"{t_name} = {mp_name}"))

    print(f"  Q1: Interface point activated (< 0.02°)? {'YES' if q1_hits else 'NO'}")
    for orb, desc in sorted(q1_hits):
        print(f"      -> {desc} at {orb:.6f}°")

    print(f"  Q2: Self-referential midpoint (< 0.01°)? {'YES' if q2_hits else 'NO'}")
    for orb, desc in sorted(q2_hits):
        print(f"      -> {desc} at {orb:.6f}°")

    q3 = bool(q1_hits and q2_hits)
    print(f"  Q3: Both in same hour? {'YES — COMPOUND DETONATION' if q3 else 'NO'}")

    all_hits = [(o, 'iface') for o, _ in q1_hits] + [(o, 'self') for o, _ in q2_hits]
    if all_hits:
        tightest = min(o for o, _ in all_hits)
        label = ("ONTOLOGICAL" if tightest < 0.001 else
                 "SIGNIFICANT" if tightest < 0.01 else
                 "MINOR" if tightest < 0.02 else "BELOW THRESHOLD")
        print(f"  Q4: Tightest orb: {tightest:.6f}° — {label}")
    else:
        print(f"  Q4: No hits below threshold. SILENCE (Rule 4 — free will).")

    # --- PHASE 5: Exactitude search for tight hits ---
    if iface_trad:
        print(f"\n{'='*80}")
        print("  PHASE 5: EXACTITUDE SEARCH (second-by-second)")
        print(f"{'='*80}")

        for _, t_name, asp_name, ip_name in iface_trad:
            if _ > 0.1:
                continue
            asp_angle = ALL_ASPECTS[asp_name]
            # Minute search
            best_orb = 999
            best_ut = 0
            for minute in range(1440):
                ut_m = minute / 60.0
                jd_m = swe.julday(t_year, t_month, t_day, ut_m)
                pos = swe.calc_ut(jd_m, PLANETS.get(t_name, swe.SUN))[0][0]
                sep = min_sep(pos, natal[ip_name])
                orb = check_aspect(sep, asp_angle)
                if orb < best_orb:
                    best_orb = orb
                    best_ut = ut_m

            # Second search around best minute
            best_orb2 = 999
            best_ut2 = 0
            start_sec = max(0, int((best_ut - 0.05) * 3600))
            end_sec = min(86400, int((best_ut + 0.05) * 3600))
            for sec in range(start_sec, end_sec):
                ut_s = sec / 3600.0
                jd_s = swe.julday(t_year, t_month, t_day, ut_s)
                pos = swe.calc_ut(jd_s, PLANETS.get(t_name, swe.SUN))[0][0]
                sep = min_sep(pos, natal[ip_name])
                orb = check_aspect(sep, asp_angle)
                if orb < best_orb2:
                    best_orb2 = orb
                    best_ut2 = ut_s

            local_time = best_ut2 + offset
            h = int(local_time)
            mf = (local_time - h) * 60
            m = int(mf)
            s = (mf - m) * 60
            print(f"  {t_name} {asp_name} {ip_name}:")
            print(f"    Exact at {h:02d}:{m:02d}:{s:04.1f} local")
            print(f"    Minimum orb: {best_orb2:.6f}° ({best_orb2*3600:.2f}\")")

    print(f"\n{'='*80}")
    print("  SCAN COMPLETE")
    print(f"{'='*80}")

    swe.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 cosmo_scan.py DATE TIME UTC_OFFSET")
        print("  DATE: YYYY-MM-DD")
        print("  TIME: HH:MM (local)")
        print("  UTC_OFFSET: +N or -N")
        print()
        print("Example: python3 cosmo_scan.py 2026-02-02 08:24 +2")
        sys.exit(1)

    run_scan(sys.argv[1], sys.argv[2], sys.argv[3])
