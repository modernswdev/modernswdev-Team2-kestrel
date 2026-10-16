import pytest
import sqlite3
from app.db import get_db

def user_in_db(app, email):
    with app.app_context():
        db = get_db()
        query = "SELECT * FROM users WHERE email = ?"
        result = db.execute(query, (email,)).fetchone()
        return True if result else False

def test_8_character_password(client, app):
    # Attempt to register with an 8-character password
    response = client.post(
        "/auth/register",
        data={"email": "test@example.com", "password": "12345678"},
    )
    assert response.headers["Location"] == "/auth/login"
    assert user_in_db(app, "test@example.com")

def test_short_password(client, app):
    # Attempt to register with a password shorter than 8 characters
    response = client.post(
        "/auth/register",
        data={"email": "test@example.com", "password": "1234567"},
    )
    assert b"Password must be at least 8 characters long." in response.data
    assert not user_in_db(app, "test@example.com")

def test_empty_password(client, app):
    # Attempt to register with an empty password
    response = client.post(
        "/auth/register",
        data={"email": "test@example.com", "password": ""},
    )
    assert b"Password is required." in response.data
    assert user_in_db(app, "test@example.com") is False


def test_missing_email_validation(client):
    # Attempt to register with an empty email address
    blank_email_data = {
        'email': '',
        'password': 'SecurePassword123!'
    }
    response = client.post('/auth/register', data=blank_email_data)
    assert b'Email is required.' in response.data


def test_duplicate_email_registration_fails(client, app):
    # Attempt to register the exact same email address twice
    first_signup = {'email': 'duplicate@ualr.edu', 'password': 'SecurePassword123!'}
    second_signup = {'email': 'duplicate@ualr.edu', 'password': 'DifferentPassword456!'}
    
    client.post('/auth/register', data=first_signup)
    response = client.post('/auth/register', data=second_signup)
    assert b'Email is already registered.' in response.data


# TODO: Add test for empty email. It can follow the same pattern as 
# `test_empty_password` above, but instead of passing an empty password 
# an empty email should be passed. Then assert that the error message 
# contains "Email is required." and that no users with an empty email 
# are in the database.
