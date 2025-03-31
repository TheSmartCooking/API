import datetime

import jwt
import pytest
from flask.testing import FlaskClient

from jwt_helper import JWT_SECRET_KEY, generate_access_token, generate_refresh_token


@pytest.fixture
def sample_person_id() -> int:
    """Provide a sample person ID for testing"""
    return 12345


@pytest.fixture
def sample_refresh_token(sample_person_id: int) -> str:
    """Provide a sample refresh token for testing"""
    return generate_refresh_token(sample_person_id)


@pytest.fixture
def sample_expired_token(sample_person_id) -> str:
    """Generate a deliberately expired JWT refresh token."""
    payload = {
        "person_id": sample_person_id,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(seconds=1),  # Already expired
        "iat": datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(hours=1),
        "token_type": "refresh",
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def test_refresh_token_success(client, sample_refresh_token, sample_access_token):
    """Test the refresh token endpoint with a valid token"""
    headers = {"Authorization": f"Bearer {sample_refresh_token}"}
    response = client.post("/refresh", headers=headers)

    assert response.status_code == 200
    assert "access_token" in response.json
    assert response.json["access_token"] == sample_access_token


def test_refresh_token_invalid_token(client: FlaskClient):
    """Test the refresh token endpoint with an invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/refresh", headers=headers)

    assert response.status_code == 401
    assert response.json == {"message": "Invalid token"}


def test_refresh_token_missing_token(client: FlaskClient):
    """Test the refresh token endpoint with a missing token"""
    response = client.post("/refresh")

    assert response.status_code == 401
    assert response.json == {"message": "Token is missing or improperly formatted"}


def test_refresh_token_expired_token(client: FlaskClient, sample_expired_token):
    """Test the refresh token endpoint with an expired token"""
    headers = {"Authorization": f"Bearer {sample_expired_token}"}

    response = client.post("/refresh", headers=headers)

    assert response.status_code == 401
    assert response.json == {"message": "Token has expired"}
