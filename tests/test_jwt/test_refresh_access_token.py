import jwt
import pytest

from jwt_helper import JWT_REFRESH_TOKEN_EXPIRY, JWT_SECRET_KEY, generate_refresh_token


@pytest.fixture
def sample_refresh_token(sample_person_id):
    """Provide a sample refresh token for testing"""
    return generate_refresh_token(sample_person_id)


def test_refresh_token_type(sample_refresh_token):
    """Ensure generate_refresh_token returns a string"""
    assert isinstance(sample_refresh_token, str)


def test_decoded_refresh_token_decoded(sample_person_id, sample_refresh_token):
    """
    Ensure the generated refresh token can be decoded and contains the correct payload
    - Check if the payload contains the correct person ID
    - Check if the token has an expiration time
    - Check if the token type is 'refresh'
    """
    decoded_payload = jwt.decode(
        sample_refresh_token, JWT_SECRET_KEY, algorithms=["HS256"]
    )

    assert decoded_payload["person_id"] == sample_person_id
    assert "exp" in decoded_payload
    assert decoded_payload["token_type"] == "refresh"


def test_refresh_token_expiration(sample_refresh_token):
    """
    Ensure the generated refresh token has a valid expiration time
    - Check if the expiration time is greater than 0
    - Check if the expiration time is greater than the issued at time
    - Check if the token is not expired
    """
    decoded_payload = jwt.decode(
        sample_refresh_token, JWT_SECRET_KEY, algorithms=["HS256"]
    )

    assert decoded_payload["exp"] > 0
    assert decoded_payload["exp"] > decoded_payload["iat"]
    assert (decoded_payload["exp"] - decoded_payload["iat"]) > JWT_REFRESH_TOKEN_EXPIRY.total_seconds()
