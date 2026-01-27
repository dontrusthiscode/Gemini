import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM EEST (UTC+3)
# Chisinau: 46.9809, 28.8704

def get_points():
    jd = swe.julday(2007, 4, 24, 1.25)
    lat = 46.9809
    lon = 28.8704
    
    # Houses and Points
    res, ascmc = swe.houses(jd, lat, lon, b'P')
    vertex = ascmc[3]
    
    # Planets
    mercury, _ = swe.calc_ut(jd, swe.MERCURY)
    neptune, _ = swe.calc_ut(jd, swe.NEPTUNE)
    venus, _ = swe.calc_ut(jd, swe.VENUS)
    mars, _ = swe.calc_ut(jd, swe.MARS)
    lilith, _ = swe.calc_ut(jd, swe.MEAN_APOG)
    
    print(f"Vertex: {vertex:.4f}")
    print(f"Mercury: {mercury[0]:.4f}")
    print(f"Neptune: {neptune[0]:.4f}")
    print(f"Venus: {venus[0]:.4f}")
    print(f"Mars: {mars[0]:.4f}")
    print(f"Lilith (Mean): {lilith[0]:.4f}")

get_points()
