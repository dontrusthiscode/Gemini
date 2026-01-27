import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM EEST (UTC+3)
# Chisinau: 46.9809, 28.8704

def audit_vibrations():
    jd = swe.julday(2007, 4, 24, 1.25)
    lat = 46.9809
    lon = 28.8704
    
    # Neptune (ID 8)
    neptune, _ = swe.calc_ut(jd, swe.NEPTUNE)
    n_long = neptune[0]
    
    # Vertex (ascmc[3])
    res, ascmc = swe.houses(jd, lat, lon, b'P')
    vertex = ascmc[3]
    
    # 12th House Cusp
    cusp_12 = res[11]
    
    print(f"Neptune Longitude: {n_long:.4f}")
    print(f"Vertex Longitude: {vertex:.4f}")
    print(f"12th House Cusp: {cusp_12:.4f}")
    
    # Aspects
    # Is Neptune conjunct Cusp 12?
    # Neptune: 321.77 (21°46' Aquarius)
    # Cusp 12: 302.00 (02°00' Aquarius)
    # Neptune is deep in the 12th.
    
    # Quincunx check: Neptune (321.77) and Vertex (219.86?)
    # Quincunx = 150 deg.
    # 321.77 - 219.86 = 101.91 (Not a quincunx, wait).
    
    # Let me re-check my previous "0.05 orb" claim.
    # In my previous session, I might have used a different point or I misread.
    # Let's check for other Neptune aspects.
    
    # Mercury is at 23°28' Aries (23.46)
    # Neptune is at 21°46' Aquarius (321.77)
    # Sextile check: 23.46 (Aries) vs 321.77 (Aquarius). 
    # 23.46 - (-38.23) = 61.69. Sextile within 1.7°. 
    
    # Let's check Vertex aspects again. 
    # Vertex is at 219.86 (Scorpio 09°51')
    # Scorpio 9.86 vs Aquarius 21.77. 
    # Scorpio to Aquarius is a Square. 
    # 21.77 (Aquarius) - 9.86 (Scorpio) = 11.91° (No).

    # Wait, check Vertex to SUN.
    # Sun is at 3.50 Taurus (33.5).
    # Vertex is 219.86 (Scorpio 9.86).
    # Opposition check: 219.86 - 33.5 = 186.36. Orb 6.36.
    
audit_vibrations()
