
def calculate_rarity():
    # 1. Mars conjunct North Node (Rahy) within 0.06 degrees
    # Probability of any two points being within 0.06 degrees:
    # 360 degrees in circle. window = 0.12 degrees (both sides).
    # P = 0.12 / 360 = 0.00033 (0.03%)
    
    # 2. Jupiter conjunct Midheaven within 0.9 degrees
    # P = 1.8 / 360 = 0.005 (0.5%)
    
    # 3. Moon at Critical Degree (0.00 to 0.99)
    # P = 1 / 30 = 0.033 (3.3%)
    
    # Compound Probability (assuming independence)
    # P_total = 0.00033 * 0.005 * 0.033
    
    mars_node_orb = 0.06
    jupiter_mc_orb = 0.9
    moon_critical = True # 00 deg 52 min
    
    p_mars_node = (mars_node_orb * 2) / 360
    p_jupiter_mc = (jupiter_mc_orb * 2) / 360
    p_moon_crit = 1 / 30 # 1 degree out of 30 per sign
    
    combined_rarity = p_mars_node * p_jupiter_mc * p_moon_crit
    one_in_x = 1 / combined_rarity
    
    print(f"Mars/NN Rarity (0.06 deg): {p_mars_node:.6f} (1 in {1/p_mars_node:.0f})")
    print(f"Jupiter/MC Rarity (0.9 deg): {p_jupiter_mc:.6f} (1 in {1/p_jupiter_mc:.0f})")
    print(f"Moon Critical Rarity (0-1 deg): {p_moon_crit:.6f} (1 in {1/p_moon_crit:.0f})")
    print(f"Combined Statistical Rarity: 1 in {one_in_x:.0f}")

if __name__ == "__main__":
    calculate_rarity()
