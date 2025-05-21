# conftest.py
import os
import pytest
from app import create_app, db

TEST_DB_PATH = "test_database.db"

@pytest.fixture(scope="function")
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{TEST_DB_PATH}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test-secret"
    })

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
