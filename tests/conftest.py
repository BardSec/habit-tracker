import pytest

from app import create_app
from app.config import Config
from app.extensions import db as _db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://habit_tracker:habit_tracker@localhost:5432/habit_tracker_test"
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "localhost"


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(autouse=True)
def session(app):
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        session = _db.session
        yield session
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(app):
    return app.test_client()
