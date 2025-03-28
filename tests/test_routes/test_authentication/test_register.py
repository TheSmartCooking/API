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


def test_missing_username(client: FlaskClient):
    """Test registration with missing username"""
    data = {
        "username": "",  # Missing username
        "email": "newuser@example.com",
        "password": "",  # Missing password
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Username, email, and password are required"


def test_missing_email(client: FlaskClient):
    """Test registration with missing email"""
    data = {
        "username": "newuser",
        "email": "",  # Missing email
        "password": "Passw0rd123!",
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Username, email, and password are required"


def test_missing_password(client: FlaskClient):
    """Test registration with missing password"""
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "",  # Missing password
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Username, email, and password are required"


def test_invalid_email(client: FlaskClient):
    """Test registration with an invalid email format"""
    data = {
        "username": "newuser",
        "email": "invalid-email",  # Invalid email format
        "password": "Passw0rd123!",
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Invalid email address"
