from datetime import datetime, timedelta

import jwt
import pytest
from flask import Flask

from jwt_helper import (
    JWT_SECRET_KEY,
    TokenError,
    extract_token_from_header,
    verify_token,
)

app = Flask(__name__)


def test_extract_token_valid(sample_token):
    """Test extracting a valid Bearer token."""
    with app.test_request_context(headers={"Authorization": f"Bearer {sample_token}"}):
        assert extract_token_from_header() == sample_token


def test_extract_token_missing():
    """Test missing Authorization header."""
    with app.test_request_context(headers={}):
        with pytest.raises(
            TokenError, match="Token is missing or improperly formatted"
        ) as excinfo:
            extract_token_from_header()
        assert excinfo.value.status_code == 401


def test_extract_token_invalid_format():
    """Test an improperly formatted Authorization header."""
    with app.test_request_context(headers={"Authorization": "InvalidTokenFormat"}):
        with pytest.raises(
            TokenError, match="Token is missing or improperly formatted"
        ) as excinfo:
            extract_token_from_header()
        assert excinfo.value.status_code == 401


def test_extract_token_no_bearer(sample_token):
    """Test Authorization header without 'Bearer ' prefix."""
    with app.test_request_context(headers={"Authorization": f"Basic {sample_token}"}):
        with pytest.raises(
            TokenError, match="Token is missing or improperly formatted"
        ) as excinfo:
            extract_token_from_header()
        assert excinfo.value.status_code == 401


def test_verify_valid_access_token():
    """Test verifying a valid access token."""
    access_token = jwt.encode(
        {"token_type": "access"}, JWT_SECRET_KEY, algorithm="HS256"
    )
    decoded = verify_token(access_token, "access")
    assert decoded["token_type"] == "access"


def test_verify_valid_refresh_token():
    """Test verifying a valid refresh token."""
    refresh_token = jwt.encode(
        {"token_type": "refresh"}, JWT_SECRET_KEY, algorithm="HS256"
    )
    decoded = verify_token(refresh_token, "refresh")
    assert decoded["token_type"] == "refresh"


def test_verify_token_invalid_type():
    """Test verifying a token with an incorrect type."""
    token = jwt.encode({"token_type": "invalid"}, JWT_SECRET_KEY, algorithm="HS256")
    with pytest.raises(TokenError, match="Invalid token") as excinfo:
        verify_token(token, "access")
    assert excinfo.value.status_code == 401


def test_verify_expired_token():
    """Test verifying an expired token."""
    expired_token = jwt.encode(
        {"token_type": "access", "exp": datetime.now() - timedelta(seconds=1)},
        JWT_SECRET_KEY,
        algorithm="HS256",
    )
    with pytest.raises(TokenError, match="Token has expired") as excinfo:
        verify_token(expired_token, "access")
    assert excinfo.value.status_code == 401


def test_verify_invalid_token():
    """Test verifying an invalid token."""
    with pytest.raises(TokenError, match="Invalid token") as excinfo:
        verify_token("invalid_token", "access")
    assert excinfo.value.status_code == 401
