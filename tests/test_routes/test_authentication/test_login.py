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
    """Test login with missing username"""
    data = {
        "username": "",  # Missing username
        "password": "Passw0rd123!",
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"


def test_missing_password(client: FlaskClient):
    """Test login with missing password"""
    data = {
        "username": "existinguser",
        "password": "",  # Missing password
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"
