import swisseph as swe
import math

swe.set_ephe_path("/Users/Admin/Documents/11_Astrology/environment/data/sweph")

# Birth Data
year, month, day = 2007, 4, 24
hour = 4 + 15/60.0 - 3.0
lat, lon = 46.9809, 28.8704
jd = swe.julday(year, month, day, hour)

# Planets
planets = {
    "Sun": swe.calc_ut(jd, swe.SUN)[0][0],
    "Moon": swe.calc_ut(jd, swe.MOON)[0][0],
    "Mercury": swe.calc_ut(jd, swe.MERCURY)[0][0],
    "Venus": swe.calc_ut(jd, swe.VENUS)[0][0],
    "Mars": swe.calc_ut(jd, swe.MARS)[0][0],
    "Jupiter": swe.calc_ut(jd, swe.JUPITER)[0][0],
    "Saturn": swe.calc_ut(jd, swe.SATURN)[0][0],
    "Uranus": swe.calc_ut(jd, swe.URANUS)[0][0],
    "Neptune": swe.calc_ut(jd, swe.NEPTUNE)[0][0],
    "Pluto": swe.calc_ut(jd, swe.PLUTO)[0][0],
    "NN": swe.calc_ut(jd, swe.TRUE_NODE)[0][0],
    "Chiron": swe.calc_ut(jd, swe.CHIRON)[0][0],
    "Lilith": swe.calc_ut(jd, swe.MEAN_APOG)[0][0] # Using Mean or True? Lilith is usually Mean Apogee (Black Moon)
}

# Angles
cusps, ascmc = swe.houses(jd, lat, lon, b'P')
angles = {
    "ASC": ascmc[0],
    "MC": ascmc[1],
    "DSC": (ascmc[0] + 180) % 360,
    "IC": (ascmc[1] + 180) % 360
}

# 1. FIXED STARS (The Royal & The Cursed)
# Algol, Regulus, Antares, Aldebaran, Fomalhaut, Spica, Sirius, Betelgeuse.
# We need star positions.
stars = [
    "Algol", "Regulus", "Antares", "Aldebaran", "Fomalhaut", "Spica", "Sirius", "Betelgeuse"
]
print("--- FIXED STAR SCANS (Orb 1.5 deg) ---")
for star in stars:
    try:
        # returns ((lon, lat, dist), name)
        res = swe.fixstar2_ut(star, jd)
        star_lon = res[0][0]
        # Check against Planets and Angles
        for pname, plon in planets.items():
            dist = abs(plon - star_lon)
            if dist > 180: dist = 360 - dist
            if dist < 1.5:
                print(f"MATCH: {star} conjunct {pname} (Orb: {dist:.4f})")
        for aname, alon in angles.items():
            dist = abs(alon - star_lon)
            if dist > 180: dist = 360 - dist
            if dist < 1.5:
                print(f"MATCH: {star} conjunct {aname} (Orb: {dist:.4f})")
    except:
        print(f"Error calculating {star}")

# 2. DRACONIC CHART overlay
# Draconic Offset = NN - 0 Aries.
# Draconic Planet = Tropical Planet - NN? No.
# Draconic is measured from the Node. 0 Aries Draconic = True Node Tropical.
# Formula: Draconic Pos = Tropical Pos - True Node. (If result < 0 add 360).
# Let's verify: If Sun is at Node, Sun Draconic should be 0 Aries.
# Tropical Node = X. Tropical Sun = X. X - X = 0. Correct.
print("\n--- DRACONIC OVERLAYS (Soul -> Reality) ---")
node_pos = planets["NN"]
for pname, plon in planets.items():
    draconic_lon = (plon - node_pos) % 360
    # Does this Draconic Planet hit a Natal Angle or Planet?
    # Check Natal Angles (Core Structure)
    for aname, alon in angles.items():
        dist = abs(draconic_lon - alon)
        if dist > 180: dist = 360 - dist
        if dist < 1.5:
            print(f"MATCH: Draconic {pname} ({draconic_lon:.2f}) conjunct Natal {aname} ({alon:.2f})")
    
    # Check Natal Planets
    for npname, nplon in planets.items():
        dist = abs(draconic_lon - nplon)
        if dist > 180: dist = 360 - dist
        if dist < 1.0: # Tighter orb for Planet-Planet
            print(f"MATCH: Draconic {pname} ({draconic_lon:.2f}) conjunct Natal {npname} ({nplon:.2f})")

# 3. MIDPOINTS (The Secret Structure)
# Sun/Moon (Inner Marriage)
# Mars/Saturn (The Drive/Brake)
# Mars/Pluto (The Force)
# Jupiter/Pluto (The Wealth)
def get_midpoint(p1, p2):
    # Shortest arc midpoint
    diff = abs(p1 - p2)
    if diff > 180:
        # Crosses 0/360
        mp = (p1 + p2 + 360) / 2
    else:
        mp = (p1 + p2) / 2
    return mp % 360

midpoints = {
    "Sun/Moon": get_midpoint(planets["Sun"], planets["Moon"]),
    "Mars/Saturn": get_midpoint(planets["Mars"], planets["Saturn"]),
    "Mars/Pluto": get_midpoint(planets["Mars"], planets["Pluto"]),
    "Jupiter/Pluto": get_midpoint(planets["Jupiter"], planets["Pluto"])
}

print("\n--- CRITICAL MIDPOINT HITS (Orb 1.0 deg) ---")
for mpname, mplon in midpoints.items():
    # Check if any planet or angle sits on this midpoint
    for pname, plon in planets.items():
        dist = abs(plon - mplon)
        if dist > 180: dist = 360 - dist
        if dist < 1.0:
            print(f"MATCH: {pname} on {mpname} (Orb: {dist:.4f})")
    for aname, alon in angles.items():
        dist = abs(alon - mplon)
        if dist > 180: dist = 360 - dist
        if dist < 1.0:
            print(f"MATCH: {aname} on {mpname} (Orb: {dist:.4f})")

# 4. LILITH CHECK
print(f"\n--- LILITH (The Taboo) ---")
print(f"Lilith Pos: {planets['Lilith']:.4f}")
# Check aspects to angles/luminaries
for aname, alon in angles.items():
    dist = abs(alon - planets['Lilith'])
    if dist > 180: dist = 360 - dist
    if dist < 2.0:
        print(f"Lilith conjunct {aname}!")
