from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

import jwt
from flask import jsonify, request

PRIVATE_KEY_PATH = Path("keys/private_key.pem")
PUBLIC_KEY_PATH = Path("keys/public_key.pem")
JWT_ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRY = timedelta(days=30)

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()


class TokenError(Exception):
    """Custom exception for token-related errors."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def generate_access_token(person_id: int) -> str:
    payload = {
        "person_id": person_id,
        "exp": datetime.now(timezone.utc) + JWT_ACCESS_TOKEN_EXPIRY,  # Expiration
        "iat": datetime.now(timezone.utc),  # Issued at
        "token_type": "access",
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def generate_refresh_token(person_id: int) -> str:
    """Generate a long-lived refresh token for a user."""
    payload = {
        "person_id": person_id,
        "exp": datetime.now(timezone.utc) + JWT_REFRESH_TOKEN_EXPIRY,  # Expiration
        "iat": datetime.now(timezone.utc),  # Issued at
        "token_type": "refresh",
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def extract_token_from_header() -> str:
    """Extract the Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise TokenError("Token is missing or improperly formatted", 401)
    return auth_header.split("Bearer ")[1]


def verify_token(token: str, required_type: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        if decoded.get("token_type") != required_type:
            raise jwt.InvalidTokenError("Invalid token type")
        return decoded
    except jwt.ExpiredSignatureError:
        raise TokenError("Token has expired", 401)
    except jwt.InvalidTokenError:
        raise TokenError("Invalid token", 401)


def token_required(f):
    """Decorator to protect routes by requiring a valid token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = extract_token_from_header()
            decoded = verify_token(token, required_type="access")
            request.person_id = decoded["person_id"]
            return f(*args, **kwargs)
        except TokenError as e:
            return jsonify(message=e.message), e.status_code

    return decorated
