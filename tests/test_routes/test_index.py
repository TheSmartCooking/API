import pytest

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get("/")
    expected_response = '{"data":{"message":"Hello there!"},"success":true}'

    assert response.status_code == 200
    assert response.data.decode("utf-8").strip() == expected_response
