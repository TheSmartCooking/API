from flask import request

from jwtoken.exceptions import TokenError


def extract_token_from_header() -> str:
    """Extract the Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise TokenError("Token is missing or improperly formatted", 401)
    return auth_header.split("Bearer ")[1]


def get_active_kid():
    with open("keys/active_kid.txt", "r") as f:
        return f.read().strip()


def load_private_key(kid):
    with open(f"keys/{kid}/private.pem", "rb") as f:
        return f.read()


def load_public_key(kid):
    try:
        with open(f"keys/{kid}/public.pem", "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise TokenError("Unknown key ID", 401)
