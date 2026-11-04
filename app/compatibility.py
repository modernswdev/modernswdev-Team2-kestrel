import os
import csv
import math

def lookup_coordinates(zip_code):
    """
    Reads the official offline GeoNames dataset (app/zip_codes.csv) 
    to extract precise nationwide coordinates.
    """
    if not zip_code:
        return None
        
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'zip_codes.csv')
    
    if not os.path.exists(csv_path):
        return None

    # GeoNames files use hidden tabs ('\t') to split data columns
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            # Column 2 (index 1) is the ZIP. Column 10 (index 9) is Latitude. Column 11 (index 10) is Longitude.
            if len(row) > 10 and row[1].strip() == str(zip_code).strip():
                return float(row[9]), float(row[10])
                
    return None

def calculate_miles(coord1, coord2):
    """
    Uses the mathematical Haversine formula to compute the exact straight-line 
    distance in miles between two coordinates. (Completely replaces geopy!)
    """
    if not coord1 or not coord2:
        return None
        
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 3956 miles is the radius of the Earth
    return 3956 * c

def score(dog_a, dog_b, miles):
    """
    Calculates compatibility between two dogs.
    Weighting: Temperament x3, Energy x2, Size x1 (Out of 24 max points)
    """
    # 1. Calculate Distance Penalty
    if miles is None:
        distance_penalty = 3.0
    elif miles <= 15:
        distance_penalty = 0.0  # Local tier
    elif miles <= 50:
        distance_penalty = 1.5  # Mid-distance tier
    else:
        distance_penalty = 3.0  # Long distance tier

    # 2. Calculate Attribute Differences (matching keys in app/dogs.py)
    size_diff = abs(dog_a['size'] - dog_b['size'])
    energy_diff = abs(dog_a['energy_level'] - dog_b['energy_level'])
    temp_diff = abs(dog_a['temperament'] - dog_b['temperament'])

    # 3. Apply the Weighting Math
    total_penalty = (temp_diff * 3) + (energy_diff * 2) + (size_diff * 1) + distance_penalty

    # 4. Turn penalty into a score out of 24 max points
    raw_score = 24.0 - total_penalty
    final_score = max(0.0, min(24.0, raw_score))
    
    return final_score
