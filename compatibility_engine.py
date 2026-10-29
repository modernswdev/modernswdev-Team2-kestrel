# compatibility_engine.py

# IMPORTING EXTERNAL LIBRARIES
# We use geopy.distance as researched by [EL] for industry-standard mileage math.
try:
    from geopy.distance import geodesic
except ImportError:
    # If the user hasn't installed geopy yet, we provide a helpful reminder
    raise ImportError("Please run 'pip install geopy' in your terminal before running this script.")


def calculate_compatibility(dog1_traits, dog2_traits, dog1_coords, dog2_coords):
    """
    Calculates the final compatibility percentage between two dogs based on 
    personality trait weights and a geographic proximity divisor.
    
    :param dog1_traits: dict with keys 'temperament', 'energy', 'size' (values 1-5)
    :param dog2_traits: dict with keys 'temperament', 'energy', 'size' (values 1-5)
    :param dog1_coords: tuple (latitude, longitude) or None if ZIP is invalid
    :param dog2_coords: tuple (latitude, longitude) or None if ZIP is invalid
    :return: float (Final Compatibility Percentage)
    """
    
    # -------------------------------------------------------------------------
    # STEP 1: Calculate Personality Baseline %
    # -------------------------------------------------------------------------
    # Extract absolute trait differences between Dog 1 and Dog 2
    temp_diff = abs(dog1_traits['temperament'] - dog2_traits['temperament'])
    energy_diff = abs(dog1_traits['energy'] - dog2_traits['energy'])
    size_diff = abs(dog1_traits['size'] - dog2_traits['size'])
    
    # Apply priority weights: Temperament (3), Energy (2), Size (1)
    total_penalty = (temp_diff * 3) + (energy_diff * 2) + (size_diff * 1)
    max_possible_penalty = 24.0
    
    # Compute the baseline percentage
    personality_baseline = 100.0 - ((total_penalty / max_possible_penalty) * 100.0)
    
    # -------------------------------------------------------------------------
    # STEP 2: Determine Proximity Divisor
    # -------------------------------------------------------------------------
    # Fallback Error Handling: If either coordinate lookup returned None (invalid ZIP), 
    # automatically assign the maximum 3.0 location divisor to prevent server crashes.
    if dog1_coords is None or dog2_coords is None:
        location_divisor = 3.0
    else:
        # Compute raw center-to-center mileage using geopy
        miles = geodesic(dog1_coords, dog2_coords).miles
        
        # Map raw distances into the 5 geographic tiers specified by [EL]
        if miles <= 15:
            location_divisor = 1.0   # Tier 1: 0–15 miles
        elif miles <= 30:
            location_divisor = 1.5   # Tier 2: 16–30 miles
        elif miles <= 60:
            location_divisor = 2.0   # Tier 3: 31–60 miles
        elif miles <= 100:
            location_divisor = 2.5   # Tier 4: 61–100 miles
        else:
            location_divisor = 3.0   # Tier 5: 101+ miles

    # -------------------------------------------------------------------------
    # STEP 3: Compute & Return Final Compatibility %
    # -------------------------------------------------------------------------
    final_compatibility = personality_baseline / location_divisor
    return round(final_compatibility, 2)


# =============================================================================
# TEST LAB / RUNNABLE EXAMPLES
# =============================================================================
if __name__ == "__main__":
    print("--- Running Compatibility Engine Test Cases ---\n")
    
    # Test Data Set: Define traits (Scale 1-5)
    buddy_traits = {'temperament': 4, 'energy': 4, 'size': 3}  # Outgoing, Athletic, Medium
    luna_traits  = {'temperament': 3, 'energy': 3, 'size': 3}  # Neutral, Balanced, Medium
    
    # Coordinates mapping (Simulating database outputs for latitude/longitude)
    raleigh_coords = (35.7796, -78.6382)
    durham_coords  = (35.9940, -78.8986)   # ~22 miles from Raleigh (Tier 2)
    charlotte_coords = (35.2271, -80.8431) # ~130 miles from Raleigh (Tier 5)
    
    # CASE 1: Local Match (Tier 2 local drive commute, 16-30 miles)
    score_local = calculate_compatibility(buddy_traits, luna_traits, raleigh_coords, durham_coords)
    print(f"Case 1 (Local Match ~22 mi): {score_local}%")
    
    # CASE 2: Long Distance Match (Tier 5, 101+ miles)
    score_far = calculate_compatibility(buddy_traits, luna_traits, raleigh_coords, charlotte_coords)
    print(f"Case 2 (Long Distance ~130 mi): {score_far}%")
    
    # CASE 3: Fallback handling (Invalid/Missing ZIP code returns None)
    score_fallback = calculate_compatibility(buddy_traits, luna_traits, raleigh_coords, None)
    print(f"Case 3 (Fallback Invalid ZIP): {score_fallback}%")
