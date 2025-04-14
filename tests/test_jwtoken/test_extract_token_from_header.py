import pytest
from flask import Flask

from jwtoken.exceptions import TokenError
from utility.jwtoken.common import extract_token_from_header

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
