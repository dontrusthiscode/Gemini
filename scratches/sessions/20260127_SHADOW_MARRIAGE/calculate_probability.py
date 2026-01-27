
import math

def calculate_probability():
    # Probability of an Antiscia Lock within 0.23 degrees
    # Total Zodiac = 360 degrees
    # For any A, the Antiscia point B is a specific point.
    # We are looking for a match within +/- 0.23 degrees.
    # Total window = 0.46 degrees.
    
    total_space = 360.0
    window = 0.46
    
    # Probability for ONE pair
    prob_single_pair = window / total_space
    
    # Rarity (1 in X)
    rarity = 1 / prob_single_pair
    
    print(f"Probability of 0.23° Antiscia lock (Single Pair): {prob_single_pair:.6f}")
    print(f"Rarity: 1 in {int(rarity)}")
    
    # Relative to the specific planets (Mars/Juno)
    # If we consider 10 main planets + Asc/MC/Nodes, many pairs are possible.
    # But specifically Juno (Marriage) and Mars (1st House Ruler/Engine)
    # The significance increases.

if __name__ == "__main__":
    calculate_probability()
