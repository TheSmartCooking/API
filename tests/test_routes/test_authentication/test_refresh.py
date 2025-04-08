import datetime

import jwt
import pytest
from flask.testing import FlaskClient

from jwt_helper import generate_refresh_token, get_active_kid, load_private_key


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
    kid = get_active_kid()
    private_key = load_private_key(kid)

    payload = {
        "person_id": sample_person_id,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(seconds=1),  # Already expired
        "iat": datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(hours=1),
        "token_type": "refresh",
    }

    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": kid})


def test_refresh_token_success(client: FlaskClient, sample_refresh_token):
    """Test the refresh token endpoint with a valid token"""
    headers = {"Authorization": f"Bearer {sample_refresh_token}"}
    response = client.post("/refresh", headers=headers)

    assert response.status_code == 200
    encoded_token = response.json["access_token"]

    # Decode the returned access token using RS256
    unverified_header = jwt.get_unverified_header(encoded_token)
    kid = unverified_header["kid"]
    public_key_path = f"keys/{kid}/public.pem"
    with open(public_key_path, "rb") as f:
        public_key = f.read()

    token = jwt.decode(encoded_token, public_key, algorithms=["RS256"])

    assert "person_id" in token
    assert "exp" in token
    assert "iat" in token
    assert token["token_type"] == "access"


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
