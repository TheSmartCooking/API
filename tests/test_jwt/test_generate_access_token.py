import jwt

from jwt_helper import JWT_ACCESS_TOKEN_EXPIRY, JWT_SECRET_KEY


def test_access_token_type(sample_access_token):
    """Ensure generate_access_token returns a string"""
    assert isinstance(sample_access_token, str)


def test_decoded_access_token(sample_person_id, sample_access_token):
    """
    Ensure the generated access token can be decoded and contains the correct payload
    - Check if the payload contains the correct person ID
    - Check if the token has an expiration time
    - Check if the token type is 'access'
    """
    payload = jwt.decode(sample_access_token, JWT_SECRET_KEY, algorithms=["HS256"])

    assert payload["person_id"] == sample_person_id
    assert "exp" in payload
    assert payload["token_type"] == "access"


def test_access_token_expiration(sample_access_token):
    """
    Ensure the generated access token has a valid expiration time
    - Check if the expiration time is greater than 0
    - Check if the expiration time is greater than the issued at time
    - Check if the token is not expired
    """
    payload = jwt.decode(sample_access_token, JWT_SECRET_KEY, algorithms=["HS256"])

    assert payload["exp"] > 0
    assert payload["exp"] > payload["iat"]
    assert (payload["exp"] - payload["iat"]) == JWT_ACCESS_TOKEN_EXPIRY.total_seconds()
