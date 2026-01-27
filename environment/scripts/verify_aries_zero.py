import swisseph as swe

swe.set_ephe_path("/Users/Admin/Documents/11_Astrology/environment/data/sweph")

# Birth Data
year, month, day = 2007, 4, 24
hour = 4 + 15/60.0 - 3.0
lat, lon = 46.9809, 28.8704
jd = swe.julday(year, month, day, hour)

# Tropical Positions
mars = swe.calc_ut(jd, swe.MARS)[0][0]
nn = swe.calc_ut(jd, swe.TRUE_NODE)[0][0]

# Draconic Calculation
# Draconic Position = Tropical Position - Mean Node? Or True Node? 
# Usually True Node for precision, but some schools use Mean.
# We will check both to see which one hits 'Zero' better.
# Formula: D_Pos = T_Pos - Node (+360)

draconic_mars_true = (mars - nn) % 360

# Check Mean Node
nn_mean = swe.calc_ut(jd, swe.MEAN_NODE)[0][0]
draconic_mars_mean = (mars - nn_mean) % 360

print(f"--- ARIES ZERO INVESTIGATION ---")
print(f"Tropical Mars: {mars:.4f} ({mars/30:.2f} deg in Sign)")
print(f"Tropical True Node: {nn:.4f}")
print(f"Tropical Mean Node: {nn_mean:.4f}")
print(f"-------------------------------")
print(f"Draconic Mars (True Node): {draconic_mars_true:.4f}")
print(f"  -> In Degrees Aries: {draconic_mars_true:.4f}")
print(f"  -> Is it 0 Aries? (360/0): Distance = {min(abs(draconic_mars_true-0), abs(draconic_mars_true-360)):.4f}")
print(f"Draconic Mars (Mean Node): {draconic_mars_mean:.4f}")

# Interpretation logic
# 0 Aries = 0.00.
# If Draconic Mars is 359.8 or 0.1, it is the "Aries Point".

# Also check if anything else is at 0 Aries.
# Perhaps the "Aries Point" itself (0 Aries) falls on a Natal Planet?
# 0 Aries Tropical is 0 Aries.
# But does 0 Aries Draconic match something?
# 0 Aries Draconic = True Node Tropical.
# So if Node is at 13 Pisces. 0 Aries Draconic is at 13 Pisces Tropical.
# User said "My Aries is at zero".
# Maybe he means "My Ascendant is 0 Aries?" No, Asc is 8 Pisces.
# Maybe "My Mars is 0 Aries Draconic?" (Most likely).

print(f"\n--- VERDICT ---")
if abs(draconic_mars_true - 0) < 1.0 or abs(draconic_mars_true - 360) < 1.0:
    print("CONFIRMED: Draconic Mars is conjunct 0 Aries (The Beginning of Time).")
else:
    print("NEGATIVE: Draconic Mars is not at 0 Aries.")
