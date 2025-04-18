from datetime import datetime, timedelta, timezone

import jwt
import pytest
from flask import Flask

from jwtoken.exceptions import TokenError
from jwtoken.tokens import (
    generate_access_token,
    generate_refresh_token,
    load_private_key,
    verify_token,
)
from utility.jwtoken.common import get_active_kid

app = Flask(__name__)


def test_verify_valid_access_token(sample_person_id):
    """Test verifying a valid access token."""
    token = generate_access_token(sample_person_id)
    decoded = verify_token(token, "access")
    assert decoded["person_id"] == sample_person_id
    assert decoded["token_type"] == "access"


def test_verify_valid_refresh_token(sample_person_id):
    """Test verifying a valid refresh token."""
    token = generate_refresh_token(sample_person_id)
    decoded = verify_token(token, "refresh")
    assert decoded["person_id"] == sample_person_id
    assert decoded["token_type"] == "refresh"


def test_verify_token_invalid_type(sample_person_id):
    """Test verifying a token with an incorrect type."""
    kid = get_active_kid()
    private_key = load_private_key(kid)

    # Create a token with token_type = "invalid"
    current_time = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "person_id": sample_person_id,
            "token_type": "invalid",
            "exp": current_time + timedelta(minutes=5),
            "iat": current_time,
        },
        private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )

    with pytest.raises(TokenError, match="Invalid token") as excinfo:
        verify_token(token, "access")
    assert excinfo.value.status_code == 401


def test_verify_expired_token(sample_person_id):
    """Test verifying an expired token."""
    kid = get_active_kid()
    private_key = load_private_key(kid)

    current_time = datetime.now(timezone.utc)
    expired_token = jwt.encode(
        {
            "person_id": sample_person_id,
            "token_type": "access",
            "exp": current_time - timedelta(seconds=1),
            "iat": current_time - timedelta(hours=1),
        },
        private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )

    with pytest.raises(TokenError, match="Token has expired") as excinfo:
        verify_token(expired_token, "access")
    assert excinfo.value.status_code == 401


def test_verify_invalid_token():
    """Test verifying a malformed or tampered token."""
    with pytest.raises(TokenError, match="Invalid token") as excinfo:
        verify_token("not_a_real_token", "access")
    assert excinfo.value.status_code == 401
