# tests/test_compatibility.py
import pytest
from app.compatibility import score

# We define standard dog profiles to pass into our function
# Your teammate noted the app stores these as 1-5 integers
dog_buddy = {'temperament': 4, 'energy_level': 4, 'size': 3}
dog_luna = {'temperament': 3, 'energy_level': 3, 'size': 3}

def test_case_1_local_match():
    # Local boundary check (e.g., 10 miles is <= 15 miles)
    # Math: Diff penalty = (1*3) + (1*2) + (0*1) = 5. Distance penalty = 0. Total = 5. 
    # Max 24 - 5 = 19.0
    result = score(dog_buddy, dog_luna, miles=10)
    assert result == 19.0

def test_case_2_long_distance_match():
    # Long distance check (e.g., 130 miles is > 50 miles)
    # Math: Diff penalty = 5. Distance penalty = 3.0. Total = 8.0. 
    # Max 24 - 8.0 = 16.0
    result = score(dog_buddy, dog_luna, miles=130)
    assert result == 16.0

def test_case_3_fallback_invalid_zip():
    # Fallback Handling (Missing or Invalid Coordinates passes None)
    # Math: Diff penalty = 5. Distance penalty = 3.0. Total = 8.0.
    # Max 24 - 8.0 = 16.0
    result = score(dog_buddy, dog_luna, miles=None)
    assert result == 16.0

def test_tier_boundary_local_exact():
    # Exact upper boundary of local tier (15 miles) should have 0 distance penalty
    result = score(dog_buddy, dog_luna, miles=15)
    assert result == 19.0

def test_tier_boundary_mid_distance_start():
    # Just past the local boundary (16 miles) jumps into the mid-distance penalty (1.5)
    # Max 24 - 5 (diff) - 1.5 (distance) = 17.5
    result = score(dog_buddy, dog_luna, miles=16)
    assert result == 17.5

def test_tier_boundary_mid_distance_exact():
    # Exact upper boundary of mid-distance tier (50 miles) should keep 1.5 distance penalty
    result = score(dog_buddy, dog_luna, miles=50)
    assert result == 17.5

def test_tier_boundary_long_distance_start():
    # Just past the mid-distance boundary (51 miles) jumps into the long-distance penalty (3.0)
    # Max 24 - 5 (diff) - 3.0 (distance) = 16.0
    result = score(dog_buddy, dog_luna, miles=51)
    assert result == 16.0
