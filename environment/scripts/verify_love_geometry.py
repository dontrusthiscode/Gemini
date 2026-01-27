import swisseph as swe
import math

swe.set_ephe_path("/Users/Admin/Documents/11_Astrology/environment/data/sweph")

# Birth Data
year, month, day = 2007, 4, 24
hour = 4 + 15/60.0 - 3.0
lat, lon = 46.9809, 28.8704
jd = swe.julday(year, month, day, hour)

# Planets
mars = swe.calc_ut(jd, swe.MARS)[0][0]
venus = swe.calc_ut(jd, swe.VENUS)[0][0]
mercury = swe.calc_ut(jd, swe.MERCURY)[0][0]
south_node = swe.calc_ut(jd, swe.TRUE_NODE)[0][0] + 180 # South Node is opp North Node

# Asteroids
# Juno = 3, Eros = 433
# Need to check if asteroid ephemeris is available or if we use approximations/search.
# Standard sweph has some. Let's try standard indices first.
# If not, we fall back to logic from encyclopedia (verified previously).
# Sweph asteroid codes: Juno=3, Vesta=4, Ceres=1, Pallas=2. Eros is se_asteroid_number('Eros')?
# Standard Indices: 
# Ceres=1, Pallas=2, Juno=3, Vesta=4
juno = swe.calc_ut(jd, swe.JUNO)[0][0]
# Eros requires specific file. We might not have it. Let's try to query '433' if fail catch.
try:
    eros = swe.calc_ut(jd, 10433)[0][0] # SE_AST_OFFSET + 433 ?? Usually swe.AST_OFFSET = 10000
except:
    eros = None

# Antiscia Calculation
# Antiscia = 360 - Longitude + 0 (Reflect over 0 Cancer/Capricorn axis i.e. 90/270 ... actually reflect over 0 Cancer/0 Cap axis?
# Solstice Axis Reflection: 
# 0 Cancer = 90 deg. 0 Cap = 270 deg.
# Formula: Antiscia = 180 - (Longitude - 90) ... No.
# Standard Formula: Antiscia = 360 - (Longitude - 0)? No.
# Antiscia is shadow point across the Solstice Axis (0 Cancer / 0 Capricorn).
# Longitude X. Antiscia = 180 - (X - 90)? 
# If 0 Aries (0) -> 0 Aries (0) NO. 0 Aries -> 0 Libra? No.
# 0 Aries (0) reflects to 0 Libra (180)? No.
# A planet at 10 Aries (10) reflects to 20 Virgo? No.
# Correct Formula: Antiscia = (90 - (Long - 90)) = 180 - Long. 
# Wait. 0 Cancer is 90. 
# Point at 80 (20 Gemini). Dis from 90 is 10. Reflected is 90+10 = 100 (10 Cancer).
# Point at 10 (10 Aries). Dis from 90 is 80. Reflected is 90+80=170 (20 Virgo).
# Formula: Antiscia = 180 - (Longitude - 0) ? No.
# Formula: Sum of Long + Antiscia = 0 Cancer + 0 Capricorn = 90 + 270 = 360? Or 180?
# Let's use the simplest: Antiscia = 300 - Long? No.
# Reflected over 0 Cancer (90) and 0 Capricorn (270).
# Mirror is the axis 0Cn-0Cp.
# If pos is 89 (29 Gem), shadow is 91 (1 Can). 89+91 = 180.
# So ANTISCIA = 180 - Longitude? 
# If Long > 180? Say 271 (1 Cap). Shadow is 269 (29 Sag). 271+269 = 540. (360+180).
# Universal Formula: (540 - Longitude) % 360.

def get_antiscia(lon):
    return (540 - lon) % 360

mars_ant = get_antiscia(mars)
venus_ant = get_antiscia(venus)
mercury_ant = get_antiscia(mercury)

# 7th House Cusp
cusps, ascmc = swe.houses(jd, lat, lon, b'P')
h7 = cusps[6]
h1 = cusps[0]

print(f"--- LOVE VECTORS ---")
print(f"Ascendant: {h1:.4f}")
print(f"Descendant (7th House): {h7:.4f} (Virgo/Pisces Axis)")
print(f"Ruler of 7th (Mercury): {mercury:.4f} (Aries)")
print(f"South Node: {south_node % 360:.4f}")
print(f"Venus: {venus:.4f} (Gemini)")
print(f"Mars: {mars:.4f} (Pisces)")
print(f"Juno: {juno:.4f}")

# Check Mars/Juno Antiscia
# Is Mars Antiscia close to Juno? Or Juno Antiscia close to Mars?
juno_ant = get_antiscia(juno)
print(f"Mars Antiscia: {mars_ant:.4f}")
print(f"Juno Antiscia: {juno_ant:.4f}")

dist_mars_juno_ant = abs(mars - juno_ant)
if dist_mars_juno_ant > 180: dist_mars_juno_ant = 360 - dist_mars_juno_ant

dist_juno_mars_ant = abs(juno - mars_ant)
if dist_juno_mars_ant > 180: dist_juno_mars_ant = 360 - dist_juno_mars_ant

print(f"Mars vs Juno Antiscia Dist: {dist_juno_mars_ant:.4f}")

# Check 7th Ruler Condition
print(f"\nRuler of 7th (Mercury) in Aries (1st House).")
print(f"Aspects to Ruler:")
print(f"Mercury-Mars Dist: {abs(mercury-mars):.4f}")
print(f"Mercury-Neptune Dist: {abs(mercury - swe.calc_ut(jd, swe.NEPTUNE)[0][0]):.4f}")

