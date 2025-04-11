from flask import request

from jwtoken.exceptions import TokenError


def extract_token_from_header() -> str:
    """Extract the Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise TokenError("Token is missing or improperly formatted", 401)
    return auth_header.split("Bearer ")[1]
