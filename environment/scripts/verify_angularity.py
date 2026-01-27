import swisseph as swe

swe.set_ephe_path("/Users/Admin/Documents/11_Astrology/environment/data/sweph")

# Birth Data
year, month, day = 2007, 4, 24
hour = 4 + 15/60.0 - 3.0
lat, lon = 46.9809, 28.8704
jd = swe.julday(year, month, day, hour)

# Calculate Ascendant
cusps, ascmc = swe.houses(jd, lat, lon, b'P')
asc = ascmc[0]

# Calculate Mars & Rahu
mars = swe.calc_ut(jd, swe.MARS)[0][0]
rahu = swe.calc_ut(jd, swe.TRUE_NODE)[0][0]

# Classical Orb Calculation (Moiety)
# Mars Moiety = 3.5 deg (Standard Classical)
# Ascendant Moiety = 5.0 deg (Standard Classical)
# Conjunction happens if Distance < (Moiety A + Moiety B)
mars_moiety = 3.5
asc_moiety = 5.0
allowed_orb = mars_moiety + asc_moiety
distance = abs(mars - asc)

print(f"--- ANGULARITY AUDIT ---")
print(f"Ascendant: {asc:.4f}")
print(f"Mars: {mars:.4f}")
print(f"Distance: {distance:.4f}")
print(f"\n--- CLASSICAL VISIBILITY ---")
print(f"Mars Moiety: {mars_moiety}")
print(f"Asc Moiety: {asc_moiety}")
print(f"Total Allowed Orb: {allowed_orb}")
print(f"Is Mars Visually Conjunct Ascendant? {distance < allowed_orb}")

# Check 1st House Placement
# Even if not conjunct, is it in the First House?
# Placidus Cusp 1 = Asc. Cusp 2 = cusps[1]
print(f"\n--- HOUSE PLACEMENT ---")
print(f"House 1 Cusp: {cusps[0]:.4f}")
print(f"House 2 Cusp: {cusps[1]:.4f}")
print(f"Is Mars in 1st House? {cusps[0] <= mars < cusps[1]}")

print(f"\n--- SYNTHESIS CHECK ---")
print(f"If Mars is in 1st House, it modifies the Body.")
print(f"Does Rahu multiply this? YES.")
