import jwt
import pytest

from jwt_helper import JWT_REFRESH_TOKEN_EXPIRY, generate_refresh_token, load_public_key


@pytest.fixture
def sample_refresh_token(sample_person_id):
    """Provide a sample refresh token for testing"""
    return generate_refresh_token(sample_person_id)


def test_refresh_token_type(sample_refresh_token):
    """Ensure generate_refresh_token returns a string"""
    assert isinstance(sample_refresh_token, str)


def test_decoded_refresh_token_decoded(
    sample_person_id, sample_refresh_token, sample_kid
):
    """
    Ensure the generated refresh token can be decoded and contains the correct payload
    - Check if the payload contains the correct person ID
    - Check if the token has an expiration time
    - Check if the token type is 'refresh'
    """

    public_key = load_public_key(sample_kid)

    payload = jwt.decode(sample_refresh_token, public_key, algorithms=["RS256"])

    assert payload["person_id"] == sample_person_id
    assert "exp" in payload
    assert payload["token_type"] == "refresh"


def test_refresh_token_expiration(sample_refresh_token, sample_kid):
    """
    Ensure the generated refresh token has a valid expiration time
    - Check if the expiration time is greater than 0
    - Check if the expiration time is greater than the issued at time
    - Check if the token is not expired
    """
    public_key = load_public_key(sample_kid)

    payload = jwt.decode(sample_refresh_token, public_key, algorithms=["RS256"])

    assert payload["exp"] > 0
    assert payload["exp"] > payload["iat"]
    assert (payload["exp"] - payload["iat"]) == JWT_REFRESH_TOKEN_EXPIRY.total_seconds()
