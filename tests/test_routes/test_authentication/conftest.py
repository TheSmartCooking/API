import pytest
from flask import Flask

from jwt_helper import generate_access_token
from routes.authentication import authentication_blueprint


@pytest.fixture
def app():
    """Create and configure a new Flask application instance for testing"""
    app = Flask(__name__)
    app.register_blueprint(authentication_blueprint)
    return app


@pytest.fixture
def sample_email():
    return "sample.email@example.com"


@pytest.fixture
def sample_password():
    return "SecurePass123!"


@pytest.fixture
def sample_username():
    return "sampleuser"


@pytest.fixture
def sample_token():
    """Provide a sample token for testing"""
    return "mock_token_123"


@pytest.fixture
def sample_access_token(sample_person_id):
    """Provide a sample access token for testing"""
    return generate_access_token(sample_person_id)
