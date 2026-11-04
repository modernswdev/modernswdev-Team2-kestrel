import pytest
from app.db import get_db

VALID_DOG = {
    "name": "Daisy", "age": "2", "sex": "Female", "zip_code": "72204",
    "size": "2", "energy_level": "4", "temperament": "4",
}

def dog_count(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM dogs").fetchone()[0]

def test_create_dog_saves_to_account_and_shows_on_dashboard(client, auth, app):
    auth.login()
    response = client.post("/dogs/new", data=VALID_DOG)
    assert response.headers["Location"] == "/dogs/"
    with app.app_context():
        dog = get_db().execute("SELECT * FROM dogs WHERE name = 'Daisy'").fetchone()
    assert dog["owner_id"] == 1
    assert (dog["size"], dog["energy_level"], dog["temperament"]) == (2, 4, 4)
    assert b"Daisy" in client.get("/dogs/").data

@pytest.mark.parametrize(("field", "value", "message"), [
    ("name", "", b"Name is required."),
    ("age", "", b"Age is required."),
    ("sex", "", b"Sex is required."),
    ("zip_code", "", b"ZIP code must be 5 digits."),
    ("zip_code", "7220", b"ZIP code must be 5 digits."),
    ("size", "", b"Size is required."),
    ("size", "6", b"Size is required."),  # outside the 1-5 scale; the form's dropdown can't send this, a raw POST can
    ("energy_level", "", b"Energy level is required."),
    ("temperament", "", b"Temperament is required."),
])
def test_invalid_field_is_rejected(client, auth, app, field, value, message):
    auth.login()
    before = dog_count(app)
    response = client.post("/dogs/new", data={**VALID_DOG, field: value})
    assert message in response.data
    assert dog_count(app) == before

@pytest.mark.parametrize("path", ["/dogs/", "/dogs/new"])
def test_logged_out_user_is_sent_to_login(client, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"

def test_dashboard_only_shows_own_dogs(client, auth):
    auth.login()
    page = client.get("/dogs/").data
    assert b"Buddy" in page
    assert b"Max" not in page
