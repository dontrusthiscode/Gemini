import swisseph as swe
import datetime

def audit_radar():
    jd = swe.julday(2007, 4, 24, 1.25)
    
    # Mercury (ID 2)
    mercury, _ = swe.calc_ut(jd, swe.MERCURY)
    # Venus (ID 3)
    venus, _ = swe.calc_ut(jd, swe.VENUS)
    # Mars (ID 4)
    mars, _ = swe.calc_ut(jd, swe.MARS)
    # Neptune (ID 8)
    neptune, _ = swe.calc_ut(jd, swe.NEPTUNE)
    
    print(f"Mercury: {mercury[0]:.4f}")
    print(f"Venus: {venus[0]:.4f}")
    print(f"Mars: {mars[0]:.4f}")
    print(f"Neptune: {neptune[0]:.4f}")

audit_radar()
