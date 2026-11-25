import pytest
from app.db import get_db

# test_data.sql: user 1 (test@test.com) owns Buddy/Bella/Lucy, user 2 (other@other.com) owns Max/Charlie.

def block_rows(app):
    with app.app_context():
        return [tuple(r) for r in get_db().execute(
            "SELECT blocker_id, blocked_id FROM blocks").fetchall()]

def test_matches_show_other_owners_dogs_only(client, auth):
    auth.login()
    page = client.get("/matches/").data
    assert b"Max" in page and b"Charlie" in page
    assert b"Buddy" not in page

def test_blocked_match_disappears_from_matches(client, auth, app):
    auth.login()
    client.post("/matches/block/2")
    assert block_rows(app) == [(1, 2)]
    page = client.get("/matches/").data
    assert b"Max" not in page and b"Charlie" not in page

def test_blocker_disappears_from_blocked_users_matches(client, auth):
    auth.login()
    client.post("/matches/block/2")
    auth.logout()
    auth.login("other@other.com", "other")
    page = client.get("/matches/").data
    assert b"Buddy" not in page
    # ...and the blocked user cannot see the block in their blocked list either
    assert b"Buddy" not in client.get("/matches/?show=blocked").data

def test_blocked_filter_lists_blocked_users_with_unblock(client, auth):
    auth.login()
    client.post("/matches/block/2")
    page = client.get("/matches/?show=blocked").data
    assert b"Max" in page and b"Unblock" in page

def test_unblock_restores_matches_both_ways(client, auth, app):
    auth.login()
    client.post("/matches/block/2")
    client.post("/matches/unblock/2")
    assert block_rows(app) == []
    assert b"Max" in client.get("/matches/").data
    auth.logout()
    auth.login("other@other.com", "other")
    assert b"Buddy" in client.get("/matches/").data

def test_blocking_twice_is_harmless(client, auth, app):
    auth.login()
    client.post("/matches/block/2")
    client.post("/matches/block/2")
    assert block_rows(app) == [(1, 2)]

def test_cannot_block_yourself(client, auth, app):
    auth.login()
    response = client.post("/matches/block/1", follow_redirects=True)
    assert b"You cannot block yourself." in response.data
    assert block_rows(app) == []

def test_blocking_unknown_user_is_404(client, auth):
    auth.login()
    assert client.post("/matches/block/999").status_code == 404

@pytest.mark.parametrize(("method", "path"), [
    ("get", "/matches/"), ("post", "/matches/block/2"), ("post", "/matches/unblock/2"),
])
def test_logged_out_user_is_sent_to_login(client, method, path):
    response = getattr(client, method)(path)
    assert response.headers["Location"] == "/auth/login"

def test_block_requires_post(client, auth):
    auth.login()
    assert client.get("/matches/block/2").status_code == 405
