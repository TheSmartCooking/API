import pytest
from flask import Flask

from jwtoken.tokens import generate_access_token


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


@pytest.fixture
def sample_token():
    """Provide a sample token for testing"""
    return "mock_token_123"


@pytest.fixture
def sample_access_token(sample_person_id):
    """Provide a sample access token for testing"""
    return generate_access_token(sample_person_id)
