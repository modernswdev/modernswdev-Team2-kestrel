import pytest
import sqlite3
from app.db import get_db


def test_dog_owner_foreign_key_is_enforced(app):
    with app.app_context():
        db = get_db()

        with pytest.raises(sqlite3.IntegrityError) as e:
            db.execute(
                "INSERT INTO dogs "
                "(owner_id, name, age, sex, zip_code, size, energy_level, temperament) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (999, "Test Dog", 3, "Male", "72204", 3, 4, 4)
                )

        assert "FOREIGN KEY constraint failed" in str(e.value)

def test_duplicate_email_is_rejected(app):
    with app.app_context():
        db = get_db()
  
        with pytest.raises(sqlite3.IntegrityError) as e:
            db.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
                ("test@test.com", "test", "testpassword")
            )
        assert "UNIQUE constraint failed" in str(e.value)

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called