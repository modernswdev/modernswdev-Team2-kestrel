import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


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
