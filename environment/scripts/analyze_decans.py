import swisseph as swe
import math

swe.set_ephe_path("/Users/Admin/Documents/11_Astrology/environment/data/sweph")

# Birth Data
year, month, day = 2007, 4, 24
hour = 4 + 15/60.0 - 3.0
lat, lon = 46.9809, 28.8704
jd = swe.julday(year, month, day, hour)

# Calculate Positions
cusps, ascmc = swe.houses(jd, lat, lon, b'P')
asc = ascmc[0]
mars = swe.calc_ut(jd, swe.MARS)[0][0]
rahu = swe.calc_ut(jd, swe.TRUE_NODE)[0][0]

def get_decan(lon):
    sign = int(lon / 30)
    degree_in_sign = lon % 30
    decan_num = int(degree_in_sign / 10) + 1
    
    # Chaldean Rulers (Star of Magi order works backwards around zodiac?)
    # Valid Chaldean Order faces:
    # Aries: Mars, Sun, Venus
    # Taurus: Mercury, Moon, Saturn
    # Gemini: Jupiter, Mars, Sun
    # Cancer: Venus, Mercury, Moon
    # Leo: Saturn, Jupiter, Mars
    # Virgo: Sun, Venus, Mercury
    # Libra: Moon, Saturn, Jupiter
    # Scorpio: Mars, Sun, Venus
    # Sagittarius: Mercury, Moon, Saturn
    # Capricorn: Jupiter, Mars, Sun
    # Aquarius: Venus, Mercury, Moon
    # Pisces: Saturn, Jupiter, Mars
    
    chaldean_rulers = {
        11: ["Saturn", "Jupiter", "Mars"] # Pisces
    }
    
    # Triplicity Rulers (Element based)
    # Pisces (Water): Pisces (Jup/Nep), Cancer (Moon), Scorpio (Mars/Pluto)
    triplicity_rulers = {
        11: ["Jupiter/Neptune", "Moon", "Mars/Pluto"]
    }
    
    ruler_chaldean = chaldean_rulers.get(sign, ["Unknown", "Unknown", "Unknown"])[decan_num - 1]
    ruler_triplicity = triplicity_rulers.get(sign, ["Unknown", "Unknown", "Unknown"])[decan_num - 1]
    
    return decan_num, ruler_chaldean, ruler_triplicity, degree_in_sign

asc_decan = get_decan(asc)
mars_decan = get_decan(mars)
rahu_decan = get_decan(rahu)

print(f"--- DECAN ANALYSIS ---")
print(f"Ascendant: {asc:.4f} (Pisces {asc_decan[3]:.2f})")
print(f"  Decan: {asc_decan[0]}")
print(f"  Chaldean Ruler: {asc_decan[1]}")
print(f"  Triplicity Ruler: {asc_decan[2]}")

print(f"\nMars: {mars:.4f} (Pisces {mars_decan[3]:.2f})")
print(f"  Decan: {mars_decan[0]}")
print(f"  Chaldean Ruler: {mars_decan[1]}")
print(f"  Triplicity Ruler: {mars_decan[2]}")

print(f"\nRahu: {rahu:.4f} (Pisces {rahu_decan[3]:.2f})")
print(f"  Decan: {rahu_decan[0]}")
print(f"  Chaldean Ruler: {rahu_decan[1]}")
print(f"  Triplicity Ruler: {rahu_decan[2]}")
