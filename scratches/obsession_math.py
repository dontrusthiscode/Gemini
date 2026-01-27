import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM EEST (UTC+3)
jd = swe.julday(2007, 4, 24, 1.25)
lat = 46.9809
lon = 28.8704

def get_obsession_metrics():
    # Lilith (Mean Apogee)
    lilith, _ = swe.calc_ut(jd, swe.MEAN_APOG)
    l_long = lilith[0]
    
    # Lilith (True/Osculating)
    lilith_t, _ = swe.calc_ut(jd, swe.OSCU_APOG)
    lt_long = lilith_t[0]
    
    # Venus (Lord 8)
    venus, _ = swe.calc_ut(jd, swe.VENUS)
    v_long = venus[0]
    
    # Mars (1st House)
    mars, _ = swe.calc_ut(jd, swe.MARS)
    m_long = mars[0]
    
    # Sun (Taurus 03.5)
    sun, _ = swe.calc_ut(jd, swe.SUN)
    s_long = sun[0]
    
    def to_sign(long):
        idx = int(long / 30)
        deg = long % 30
        signs = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
        return f"{signs[idx]} {deg:.2f}°"

    print(f"Lilith (Mean): {to_sign(l_long)}")
    print(f"Lilith (True): {to_sign(lt_long)}")
    print(f"Venus (Lord 8): {to_sign(v_long)}")
    print(f"Mars (Friction): {to_sign(m_long)}")
    
    # Check Lilith aspects
    # Lilith (Mean) is Leo 06.07 (126.07)
    # Saturn is Leo 18.10 (138.17)
    # Moon is Leo 00.52 (120.87)
    # Lilith is exactly between Moon and Saturn? No, but close.
    
    # Vertex is 171.71 (Virgo 21.71)
    
get_obsession_metrics()
