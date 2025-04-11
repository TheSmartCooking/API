from functools import wraps

from flask import jsonify, request

from utility.jwtoken.common import extract_token_from_header

from .exceptions import TokenError
from .tokens import verify_token


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
