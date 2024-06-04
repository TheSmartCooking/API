from flask import current_app, jsonify
from flask_jwt_extended import JWTManager
from flask_limiter import RateLimitExceeded
from pymysql import DatabaseError
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    MethodNotAllowed,
    NotFound,
    RequestEntityTooLarge,
    Unauthorized,
)


def handle_database_error(error):
    current_app.logger.error(f"Database connection error: {error}")
    return jsonify(error="Database connection error"), 500


def handle_not_found_error(error):
    current_app.logger.error(f"Not found error: {error}")
    return jsonify(error="Resource not found"), 404


def handle_bad_request_error(error):
    current_app.logger.error(f"Bad request error: {error}")
    return jsonify(error="Bad request"), 400


def handle_unauthorized_error(error):
    current_app.logger.error(f"Unauthorized error: {error}")
    return jsonify(error="Unauthorized"), 401


def handle_forbidden_error(error):
    current_app.logger.error(f"Forbidden error: {error}")
    return jsonify(error="Forbidden"), 403


def handle_method_not_allowed_error(error):
    current_app.logger.error(f"Method not allowed error: {error}")
    return jsonify(error="Method not allowed"), 405


def handle_server_error(error):
    current_app.logger.error(f"Server error: {error}")
    return jsonify(error="Internal server error"), 500


def expired_token_callback(jwt_header, jwt_payload):
    current_app.logger.error(f"Token has expired: {jwt_header} | {jwt_payload}")
    return jsonify(message="Token has expired"), 401


def handle_rate_limit_exceeded_error(error):
    current_app.logger.error(f"Rate limit exceeded: {error}")
    return jsonify(error="Rate limit exceeded"), 429


def handle_request_entity_too_large_error(error):
    current_app.logger.error(f"Request entity too large: {error}")
    return jsonify(error="Request entity too large"), 413


def register_error_handlers(app):
    app.register_error_handler(DatabaseError, handle_database_error)
    app.register_error_handler(NotFound, handle_not_found_error)
    app.register_error_handler(BadRequest, handle_bad_request_error)
    app.register_error_handler(Unauthorized, handle_unauthorized_error)
    app.register_error_handler(Forbidden, handle_forbidden_error)
    app.register_error_handler(MethodNotAllowed, handle_method_not_allowed_error)
    app.register_error_handler(
        RequestEntityTooLarge, handle_request_entity_too_large_error
    )

    # Handle RateLimitExceeded before general Exception handler
    app.register_error_handler(RateLimitExceeded, handle_rate_limit_exceeded_error)

    # Initialize and configure JWTManager
    jwt = JWTManager(app)
    jwt.expired_token_loader(expired_token_callback)

    # Catch-all for other exceptions
    app.register_error_handler(Exception, handle_server_error)
