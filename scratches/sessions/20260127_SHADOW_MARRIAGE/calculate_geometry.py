
import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM (EEST)
# Coordinates: 46.9809, 28.8704 (Chisinau, Moldova)
# UTC Offset: +3

def calculate_precision():
    # Set Ephemeris Path
    swe.set_ephe_path('environment/data/sweph/')
    
    # Calculate Julian Day
    year, month, day = 2007, 4, 24
    hour = 4 + 15/60.0 - 3 # Convert EEST to UTC
    jd = swe.julday(year, month, day, hour)
    
    # Planets
    planets = {
        'Mars': swe.MARS,
        'Juno': swe.JUNO
    }
    
    results = {}
    for name, id in planets.items():
        res, ret = swe.calc_ut(jd, id, swe.FLG_SWIEPH | swe.FLG_SPEED)
        results[name] = res[0]
        
    # Calculate Antiscia for Mars
    # Antiscia Formula: 90 - (Long - 90) = 180 - Long (relative to 0 Cancer/0 Capricorn axis)
    # The axis is 0 Cancer (90°) / 0 Capricorn (270°)
    # If Long is X, Antiscia is 180 - X (Tropical)
    mars_long = results['Mars']
    mars_antiscia = (180 - mars_long) % 360
    
    juno_long = results['Juno']
    orb = abs(juno_long - mars_antiscia)
    if orb > 180: orb = 360 - orb
    
    print(f"Mars Longitude: {mars_long:.5f} ({swe.get_planet_name(swe.MARS)})")
    print(f"Juno Longitude: {juno_long:.5f} (Juno)")
    print(f"Mars Antiscia: {mars_antiscia:.5f}")
    print(f"Orb (Antiscia): {orb:.5f}")
    
    # Navamsa (D9) calculation
    def get_navamsa(long):
        # 3°20' per Navamsa
        nav_index = int((long % 30) / (3.3333333333))
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_index = int(long / 30)
        
        # Method: Starting from Aries for Fire, Capricorn for Earth, Libra for Air, Cancer for Water
        base_nav = [0, 9, 6, 3] # Indices for signs
        sign_type = sign_index % 4
        nav_sign_index = (base_nav[sign_type] + nav_index) % 12
        return signs[nav_sign_index]

    print(f"Mars Navamsa: {get_navamsa(mars_long)}")
    print(f"Juno Navamsa: {get_navamsa(juno_long)}")

if __name__ == "__main__":
    calculate_precision()
