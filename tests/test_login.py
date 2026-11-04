import pytest

def logged_in_user_id(client):
    with client.session_transaction() as session:
        return session.get("user_id")

def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Log In" in response.data

def test_correct_login_starts_session(client, auth):
    response = auth.login()
    assert response.headers["Location"] == "/"
    assert logged_in_user_id(client) == 1

def test_logged_in_user_shown_in_nav(client, auth):
    auth.login()
    response = client.get("/")
    assert b"<span>test</span>" in response.data
    assert b"Log Out" in response.data

@pytest.mark.parametrize(("email", "password"), [
    ("test@test.com", "wrongpassword"),  # wrong password
    ("nobody@test.com", "test"),         # unregistered email
    ("bad.email.com", "p@ssword"),       # malformed email; the browser's type="email" check doesn't run here
])
def test_bad_credentials_are_rejected(client, auth, email, password):
    # same message for every case so the form can't be used to discover registered emails
    response = auth.login(email, password)
    assert b"Incorrect email or password." in response.data
    assert logged_in_user_id(client) is None

def test_logout_clears_session(client, auth):
    auth.login()
    response = auth.logout()
    assert response.headers["Location"] == "/"
    assert logged_in_user_id(client) is None
