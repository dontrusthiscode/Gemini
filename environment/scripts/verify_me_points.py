import swisseph as swe
import sys
import os

# Set Ephemeris Path
swe.set_ephe_path("/Users/Admin/Documents/11_Astrology/environment/data/sweph")

# Birth Data (from 00_CORE_DATA.md)
# April 24, 2007, 04:15 AM (EEST = UTC+3)
year, month, day = 2007, 4, 24
hour = 4 + 15/60.0 - 3.0 # Convert to UTC
lat, lon = 46.9809, 28.8704

# Calculate Julian Day
jd = swe.julday(year, month, day, hour)

# Calculate Ascendant, Vertex, MC
# houses(jd, lat, lon, hsys) -> returns (cusps, ascmc)
# ascmc indices: 0=Asc, 1=MC, 2=ARMC, 3=Vertex
cusps, ascmc = swe.houses(jd, lat, lon, b'P')
asc = ascmc[0]
mc = ascmc[1]
vertex = ascmc[3]

# Calculate Planets
def get_pos(planet):
    res = swe.calc_ut(jd, planet)
    return res[0][0] # longitude

sun = get_pos(swe.SUN)
moon = get_pos(swe.MOON)
mars = get_pos(swe.MARS)
jupiter = get_pos(swe.JUPITER)
saturn = get_pos(swe.SATURN)
neptune = get_pos(swe.NEPTUNE)
rahu_mean = get_pos(swe.MEAN_NODE) # Mean Node often used for Draconic
rahu_true = get_pos(swe.TRUE_NODE) # True Node

# Calculate Part of Fortune
# Night Chart check: Sun (33.5) in House 2 (Placidus)? 
# Asc (338.68). House 2 cusp (29.66). Sun is in House 2.
# Sun is below horizon. Night Chart.
# Formula: Asc + Sun - Moon
pof = (asc + sun - moon) % 360
if pof < 0: pof += 360

# Calculations for "Me.md" claims

print(f"--- POINTS ---")
print(f"Ascendant: {asc:.4f}")
print(f"Vertex: {vertex:.4f}")
print(f"Sun: {sun:.4f}")
print(f"Moon: {moon:.4f}")
print(f"Mars: {mars:.4f}")
print(f"Jupiter: {jupiter:.4f}")
print(f"Saturn: {saturn:.4f}")
print(f"Neptune: {neptune:.4f}")
print(f"North Node (True): {rahu_true:.4f}")
print(f"Part of Fortune: {pof:.4f}")

print(f"\n--- AUDIT CHECKS ---")

# 1. Mars Conjunct Ascendant
# Claim: "Mars Conjunct Ascendant"
# My Check: Abs(Mars - Asc)
diff_mars_asc = min(abs(mars - asc), 360 - abs(mars - asc))
print(f"CLAIM 1: Mars Conjunct Ascendant Orb: {diff_mars_asc:.4f}")

# 2. Mars Conjunct North Node (Claim 0.07 orb)
diff_mars_nn = min(abs(mars - rahu_true), 360 - abs(mars - rahu_true))
print(f"CLAIM 2: Mars Conjunct Rahu Orb: {diff_mars_nn:.4f}")

# 3. Jupiter Conjunct Lot of Fortune
diff_jup_pof = min(abs(jupiter - pof), 360 - abs(jupiter - pof))
print(f"CLAIM 3: Jupiter Conjunct PoF Orb: {diff_jup_pof:.4f}")

# 4. Vertex Quincunx Neptune (Claim 0.03 orb)
# Quincunx = 150
aspect_vertex_nep = abs(vertex - neptune) % 360
# Check distance from 150 or 210
orb_q1 = abs(aspect_vertex_nep - 150)
orb_q2 = abs(aspect_vertex_nep - 210)
print(f"CLAIM 4: Vertex/Neptune Quincunx Orb: {min(orb_q1, orb_q2):.4f}")

# 5. Saturn Conjunct Moon (Draconic Interaction check requires Draconic calc)
# Draconic Point = Tropical Point - Tropical True Node
drac_moon = (moon - rahu_true) % 360
drac_saturn = (saturn - rahu_true) % 360

# Claim: Saturn Conjunct Moon via Draconic/Tropical Interaction
# Possibility A: Draconic Saturn Conjunct Tropical Moon
diff_ds_tm = min(abs(drac_saturn - moon), 360 - abs(drac_saturn - moon))
# Possibility B: Tropical Saturn Conjunct Draconic Moon
diff_ts_dm = min(abs(saturn - drac_moon), 360 - abs(saturn - drac_moon))
print(f"CLAIM 5: Saturn/Moon Draconic Interaction (DS-TM): {diff_ds_tm:.4f}")
print(f"CLAIM 5: Saturn/Moon Draconic Interaction (TS-DM): {diff_ts_dm:.4f}")
