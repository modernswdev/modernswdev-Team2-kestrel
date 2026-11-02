# copied from [https://flask.palletsprojects.com/en/2.3.x/testing/#a-minimal-application] and modified to use the app factory
import os, tempfile, pytest
from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "test_data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path})
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# logs in through the real /auth/login route; test_data.sql users' passwords match their usernames
class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="test@test.com", password="test"):
        return self._client.post(
            "/auth/login", data={"email": email, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")

@pytest.fixture
def auth(client):
    return AuthActions(client)
