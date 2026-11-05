import pytest

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"PawLink" in response.data


def test_home_page_links_manifest(client):
    response = client.get("/")
    assert b'rel="manifest"' in response.data


def test_manifest_is_valid_json(client):
    response = client.get("/static/manifest.json")
    assert response.status_code == 200
    assert response.get_json()["start_url"] == "/"


def test_service_worker_served_from_root(client):
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert response.mimetype == "application/javascript"


# ==================================================
# TEST FOR FEATURE #26: WEIGHTED COMPATIBILITY SCORING
# CONTRIBUTED BY: ELIZABETH
# ==================================================

def test_compatibility_score_is_near_maximum_for_total_mismatch(client):
    # 1. ARRANGE: Set up two completely incompatible dog profiles using our 1-5 custom scales
    dog1_profile = {
        "location": "Little Rock", 
        "temperament": "Anxious", 
        "size": "X-Large", 
        "energy": "Unconcious"
    }
    dog2_profile = {
        "location": "Fayetteville", 
        "temperament": "Chill",    
        "size": "X-Small", 
        "energy": "Energizer Bunny"
    }
    
    # 2. ACT: Run them through the scoring engine to get a numeric penalty score
    calculated_score = calculate_compatibility_score(dog1_profile, dog2_profile)
    
    # 3. ASSERT: On our 0 to 40 penalty scale (higher means worse), 
    # this extreme mismatch must trigger a massive penalty greater than 35.
    assert calculated_score > 35
