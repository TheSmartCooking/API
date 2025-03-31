import jwt
import pytest

from jwt_helper import JWT_ACCESS_TOKEN_EXPIRY, JWT_SECRET_KEY, generate_access_token


@pytest.fixture
def sample_access_token(sample_person_id):
    """Provide a sample access token for testing"""
    return generate_access_token(sample_person_id)


def test_generate_access_token_type(sample_access_token):
    """Ensure generate_access_token returns a string"""
    assert isinstance(sample_access_token, str)


def test_generate_access_token_todo():
    # Decode the token to verify its contents
    decoded_payload = jwt.decode(
        sample_access_token, JWT_SECRET_KEY, algorithms=["HS256"]
    )

    # Check if the payload contains the correct person ID
    assert decoded_payload["person_id"] == sample_person_id

    # Check if the token has an expiration time
    assert "exp" in decoded_payload

    # Check if the token type is 'access'
    assert decoded_payload["token_type"] == "access"
