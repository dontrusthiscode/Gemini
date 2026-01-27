import swisseph as swe
import datetime

# Birth Data: April 24, 2007, 04:15 AM EEST (UTC+3)
# Chisinau: 46.9809, 28.8704
lat = 46.9809
lon = 28.8704
jd = swe.julday(2007, 4, 24, 1.25)

def get_full_data():
    # Houses
    res, ascmc = swe.houses(jd, lat, lon, b'P')
    vertex = ascmc[3]
    
    # Neptune
    neptune, _ = swe.calc_ut(jd, swe.NEPTUNE)
    n_long = neptune[0]
    
    # Check for Quincunx (150 deg)
    diff = abs(n_long - vertex)
    if diff > 180: diff = 360 - diff
    
    print(f"Vertex: {vertex:.4f} ({int(vertex/30)} {vertex%30:.2f})")
    print(f"Neptune: {n_long:.4f} ({int(n_long/30)} {n_long%30:.2f})")
    print(f"Difference: {diff:.4f}")
    
    # Is there another Neptune aspect?
    # Vertex 219.86 (Scorpio 09)
    # Neptune 351 (Pisces?) Wait, let me check the SIGN index.
    # res[0] is longitude.
    # Aquarius is index 10 (300-330).
    # Pisces is index 11 (330-360).
    
    # Let me calculate all aspects between all major points and Neptune.
    points = {
        "ASC": ascmc[0],
        "MC": ascmc[1],
        "Vertex": ascmc[3],
        "Sun": swe.calc_ut(jd, swe.SUN)[0][0],
        "Moon": swe.calc_ut(jd, swe.MOON)[0][0],
        "Mercury": swe.calc_ut(jd, swe.MERCURY)[0][0],
        "Venus": swe.calc_ut(jd, swe.VENUS)[0][0],
        "Mars": swe.calc_ut(jd, swe.MARS)[0][0],
        "Jupiter": swe.calc_ut(jd, swe.JUPITER)[0][0],
        "Saturn": swe.calc_ut(jd, swe.SATURN)[0][0],
        "Uranus": swe.calc_ut(jd, swe.URANUS)[0][0],
        "Pluto": swe.calc_ut(jd, swe.PLUTO)[0][0],
        "North Node": swe.calc_ut(jd, swe.MEAN_NODE)[0][0]
    }
    
    for name, pos in points.items():
        d = abs(pos - n_long)
        if d > 180: d = 360 - d
        # Check for Quincunx (150), Square (90), Sextile (60), Trine (120), Opp (180), Conj (0).
        aspects = {0: "Conj", 60: "Sextile", 90: "Square", 120: "Trine", 150: "Quincunx", 180: "Opp"}
        for deg, a_name in aspects.items():
            if abs(d - deg) < 2.0:
                print(f"Neptune {a_name} {name} (Orb: {abs(d-deg):.2f})")

get_full_data()
