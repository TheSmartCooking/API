import pytest

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    with app.test_client() as client:
        yield client


def test_index_route_status_code(client):
    """Ensure the index route returns a 200 status code"""
    response = client.get("/")
    assert response.status_code == 200


def test_index_route_json(client):
    """Ensure the index route returns the correct JSON response"""
    response = client.get("/")
    expected_response = {"message": "Hello there!"}

    assert response.is_json
    assert response.get_json() == expected_response
