from flask import Flask, jsonify

from jwt_helper import token_required

app = Flask(__name__)


def test_token_required_valid(sample_access_token):
    """Test the token_required decorator with a valid token."""

    @token_required
    def protected_route():
        return jsonify(message="Success"), 200

    with app.test_request_context(
        headers={"Authorization": f"Bearer {sample_access_token}"}
    ):
        response = protected_route()
        assert response[1] == 200


def test_token_required_invalid_token():
    """Test the token_required decorator with an invalid token."""
    with app.test_request_context(headers={"Authorization": "Bearer invalid_token"}):

        @token_required
        def protected_route():
            return jsonify(message="Success"), 200

        response = protected_route()
        assert response[1] == 401


def test_token_required_missing_token():
    """Test the token_required decorator when no token is provided."""
    with app.test_request_context(headers={}):

        @token_required
        def protected_route():
            return jsonify(message="Success"), 200

        response = protected_route()
        assert response[1] == 401
