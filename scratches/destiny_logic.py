import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM EEST (UTC+3)
jd = swe.julday(2007, 4, 24, 1.25)
lat = 46.9809
lon = 28.8704

def analyze_destiny():
    # Houses
    res, ascmc = swe.houses(jd, lat, lon, b'P')
    cusp_5 = res[4] # Cancer 09.25
    
    # Lord of 5 (Moon)
    moon, _ = swe.calc_ut(jd, swe.MOON)
    m_long = moon[0]
    
    # Neptune
    neptune, _ = swe.calc_ut(jd, swe.NEPTUNE)
    n_long = neptune[0]
    
    # 5th House (Romance/Stories) is Cancer. Lord is Moon.
    # Moon in Leo 00.52 (120.87)
    # Neptune in Aquarius 21.46 (321.77)
    
    # Aspect check: Moon/Neptune
    diff = abs(m_long - n_long)
    if diff > 180: diff = 360 - diff
    # 321.77 - 120.87 = 200.9 -> 159.1 (Opposition/Quincunx area)
    
    # Vertex
    vertex = ascmc[3] # 171.71 (Virgo 21.71)
    
    print(f"Moon: {m_long:.4f} (Self-Image/Needs)")
    print(f"Neptune: {n_long:.4f} (The Radio)")
    print(f"Vertex: {vertex:.4f} (The Gate)")
    
    # Logic: 
    # Lord of 7 (Mercury) - The Other
    # Lord of 5 (Moon) - The Story/Romance
    # Lord of 8 (Venus) - The Friction/Sex
    
    # Mercury (Aries 23.47)
    # Moon (Leo 0.87)
    # Aspect: 120.87 - 23.47 = 97.4 (Square area)
    
analyze_destiny()
