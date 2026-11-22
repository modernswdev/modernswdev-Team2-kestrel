from app.db import get_db


def test_matches_requires_login(client):
    response = client.get("/dogs/matches")
    assert response.headers["Location"] == "/auth/login"


def test_matches_prompts_when_user_has_no_dog(client, auth, app):
    auth.login()
    with app.app_context():
        db = get_db()
        db.execute("DELETE FROM dogs WHERE owner_id = 1")
        db.commit()

    response = client.get("/dogs/matches")
    assert response.status_code == 200
    assert b"Create a dog profile first" in response.data


def test_matches_ranked_and_shows_required_details(client, auth, app):
    auth.login()
    with app.app_context():
        db = get_db()
        my_dog = db.execute("SELECT * FROM dogs WHERE owner_id = 1").fetchone()
        # Insert a perfect match (identical stats + same ZIP as user 1's dog)
        db.execute(
            "INSERT INTO dogs (owner_id, name, age, sex, zip_code, size, energy_level, temperament)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (2, "PerfectPup", 3, "Female", my_dog["zip_code"], my_dog["size"], my_dog["energy_level"], my_dog["temperament"]),
        )
        # Insert a poor match (opposite stats + far away ZIP)
        far_size = 5 if my_dog["size"] == 1 else 1
        far_energy = 5 if my_dog["energy_level"] == 1 else 1
        far_temp = 5 if my_dog["temperament"] == 1 else 1
        db.execute(
            "INSERT INTO dogs (owner_id, name, age, sex, zip_code, size, energy_level, temperament)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (2, "MismatchMutt", 4, "Male", "90210", far_size, far_energy, far_temp),
        )
        db.commit()

    response = client.get("/dogs/matches")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Verify own dog is excluded and both other dogs appear
    assert my_dog["name"] not in html
    assert "PerfectPup" in html
    assert "MismatchMutt" in html

    # Verify ranked order: PerfectPup appears before MismatchMutt
    assert html.index("PerfectPup") < html.index("MismatchMutt")

    # Verify required fields are shown (Size, Energy, Temperament, Distance)
    assert "Size:" in html
    assert "Energy:" in html
    assert "Temperament:" in html
    assert "miles away" in html
