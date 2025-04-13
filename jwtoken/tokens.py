from datetime import datetime, timedelta, timezone

import jwt

from utility.jwtoken.common import get_active_kid, load_private_key, load_public_key

from .exceptions import TokenError

JWT_ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRY = timedelta(days=30)


def generate_access_token(person_id: int) -> str:
    kid = get_active_kid()
    private_key = load_private_key(kid)

    current_time = datetime.now(timezone.utc)
    payload = {
        "person_id": person_id,
        "exp": current_time + JWT_ACCESS_TOKEN_EXPIRY,  # Expiration
        "iat": current_time,  # Issued at
        "token_type": "access",
    }
    headers = {"kid": kid}
    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


def generate_refresh_token(person_id: int) -> str:
    """Generate a long-lived refresh token for a user."""
    kid = get_active_kid()
    private_key = load_private_key(kid)

    payload = {
        "person_id": person_id,
        "exp": datetime.now(timezone.utc) + JWT_REFRESH_TOKEN_EXPIRY,  # Expiration
        "iat": datetime.now(timezone.utc),  # Issued at
        "token_type": "refresh",
    }
    headers = {"kid": kid}

    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


def verify_token(token: str, required_type: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise TokenError("KID missing in token header", 401)

        public_key = load_public_key(kid)

        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        if decoded.get("token_type") != required_type:
            raise jwt.InvalidTokenError("Invalid token type")
        return decoded

    except jwt.ExpiredSignatureError:
        raise TokenError("Token has expired", 401)
    except jwt.InvalidTokenError:
        raise TokenError("Invalid token", 401)
