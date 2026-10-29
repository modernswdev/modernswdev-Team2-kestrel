# test_compatibility.py
import pytest

# Test the core math engine parameters defined by [EL] in the scratchpad
def calculate_test_score(t1, t2, size1, size2, energy1, energy2, is_local_commute, is_long_distance, is_fallback):
    temp_diff = abs(t1 - t2)
    energy_diff = abs(energy1 - energy2)
    size_diff = abs(size1 - size2)
    
    penalty = (temp_diff * 3) + (energy_diff * 2) + (size_diff * 1)
    base_score = 100.0 - ((penalty / 24.0) * 100.0)
    
    if is_fallback or is_long_distance:
        divisor = 3.0
    elif is_local_commute:
        divisor = 1.5
    else:
        divisor = 1.0
        
    return round(base_score / divisor, 2)

def test_case_1_local_match():
    # Buddy vs Luna Local Drive Commute (~22 miles)
    score = calculate_test_score(4, 3, 3, 3, 4, 3, is_local_commute=True, is_long_distance=False, is_fallback=False)
    assert score == 52.78

def test_case_2_long_distance_match():
    # Buddy vs Luna Long Distance (~130 miles)
    score = calculate_test_score(4, 3, 3, 3, 4, 3, is_local_commute=False, is_long_distance=True, is_fallback=False)
    assert score == 26.39

def test_case_3_fallback_invalid_zip():
    # Fallback Handling (Missing or Invalid Coordinates)
    score = calculate_test_score(4, 3, 3, 3, 4, 3, is_local_commute=False, is_long_distance=False, is_fallback=True)
    assert score == 26.39
