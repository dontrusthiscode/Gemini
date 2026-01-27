import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM EEST (UTC+3)
# Chisinau, Moldova: 46.9809, 28.8704

def get_juno():
    # UTC Time: 01:15 AM
    jd = swe.julday(2007, 4, 24, 1.25)
    
    # Calculate Juno (ID 19)
    res, ret = swe.calc_ut(jd, swe.JUNO)
    longitude = res[0]
    
    sign_idx = int(longitude / 30)
    degree = longitude % 30
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    print(f"Juno: {signs[sign_idx]} {degree:.4f}°")
    
    # Antiscia calc
    # Mars is at 13.55 (13°33' Pisces)
    mars_long = 330 + 13.55
    mars_antiscia = (360 - (mars_long - 90)) % 360 # Reflected across 0 Can/Cap
    # Wait, the signs are: Pisces -> Libra
    # 0 Pisces -> 30 Libra
    # 13.55 Pisces -> (30 - 13.55) = 16.45 Libra
    
    print(f"Mars Antiscia Point: Libra {30 - 13.55:.4f}°")

get_juno()
