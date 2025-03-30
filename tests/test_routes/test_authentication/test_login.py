import pytest
from flask import Flask
from flask.testing import FlaskClient

from routes.authentication import authentication_blueprint


@pytest.fixture
def app():
    """Create and configure a new Flask application instance for testing"""
    app = Flask(__name__)
    app.register_blueprint(authentication_blueprint)
    return app


@pytest.fixture
def client(app: Flask):
    """Create a test client for the Flask application"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_email():
    return "sample.email@example.com"


@pytest.fixture
def sample_password():
    return "SecurePass123!"


@pytest.fixture
def sample_username():
    return "sampleuser"


def test_missing_username(client: FlaskClient, sample_password):
    """Test login with missing username"""
    data = {
        "username": "",  # Missing username
        "password": sample_password,
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"


def test_missing_password(client: FlaskClient, sample_username):
    """Test login with missing password"""
    data = {
        "username": sample_username,
        "password": "",  # Missing password
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"
