import argparse
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from config.logging import setup_logging
from config.ratelimit import limiter
from config.settings import Config
from routes import register_routes
from utility import extract_error_message

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
limiter.init_app(app)
logger = setup_logging()

if app.config["TESTING"]:
    limiter.enabled = False


@app.route("/")
def home():
    return jsonify(message="Hello there!")


# Register routes and error handlers
register_routes(app)


# Add a status field to all JSON responses
@app.after_request
def add_status(response):
    if response.is_json:
        original_data = response.get_json()
        new_response = {
            "success": response.status_code in range(200, 300),
            "data": original_data if original_data != [] else None,
        }
        response.set_data(jsonify(new_response).data)
    return response


@app.after_request
def add_common_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.errorhandler(429)
def ratelimit_error(e):
    logger.warning(
        f"Rate limit exceeded: {request.method} {request.path} - {e.description}"
    )
    return (
        jsonify(
            error="Too many requests",
            message="Rate limit exceeded. Please try again later.",
            rate_limit=e.description,
        ),
        429,
    )


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e

    trace = traceback.format_exc().splitlines()[-1]
    logger.exception(f"An unhandled exception occurred: {trace}")
    error_message = extract_error_message(str(e))
    return jsonify(error="Internal Server Error", message=error_message), 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask application.")
    parser.add_argument(
        "--debug", action="store_true", help="Run the app in debug mode."
    )
    args = parser.parse_args()

    logger.info("Starting Flask application...")
    app.run(host="0.0.0.0", port=5000, debug=args.debug)
