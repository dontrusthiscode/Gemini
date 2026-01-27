import swisseph as swe
import datetime

def audit_viability():
    jd = swe.julday(2007, 4, 24, 1.25)
    lat = 46.9809
    lon = 28.8704
    
    # 1st House Nuances
    res, ascmc = swe.houses(jd, lat, lon, b'P')
    asc = ascmc[0]
    
    # Lilith (ID 19 - but usually MEAN_APOG)
    lilith, _ = swe.calc_ut(jd, swe.MEAN_APOG)
    l_long = lilith[0]
    
    # Venus (Lord 8)
    venus, _ = swe.calc_ut(jd, swe.VENUS)
    v_long = venus[0]
    
    # Mars (1st House Resident)
    mars, _ = swe.calc_ut(jd, swe.MARS)
    m_long = mars[0]
    
    # Saturn (Lord 11/12 - Karma/Void)
    saturn, _ = swe.calc_ut(jd, swe.SATURN)
    s_long = saturn[0]
    
    # Moon (Self-Image)
    moon, _ = swe.calc_ut(jd, swe.MOON)
    mo_long = moon[0]
    
    print(f"ASC: {asc:.4f}")
    print(f"Mars: {m_long:.4f} (Orb to ASC: {abs(m_long-asc):.4f})")
    print(f"Venus: {v_long:.4f}")
    print(f"Lilith: {l_long:.4f}")
    print(f"Moon: {mo_long:.4f} (Leo 00° - Fixed Fire)")
    print(f"Saturn: {s_long:.4f} (Leo 18°)")
    
    # The 8th House is Libra/Scorpio?
    # House 7 is Virgo 8. House 8 is Libra 29.
    # Lord of 8 is Venus (Gemini 13). 
    
    # Venus Square Mars:
    d = abs(v_long - m_long)
    if d > 180: d = 360 - d
    print(f"Venus Square Mars Orb: {abs(d-90):.4f}")

audit_viability()
