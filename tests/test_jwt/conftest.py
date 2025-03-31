import pytest
from flask import Flask


@pytest.fixture
def client(app: Flask):
    """Create a test client for the Flask application"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_person_id() -> int:
    """Provide a sample person ID for testing"""
    return 12345
