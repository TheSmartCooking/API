import os
from datetime import timedelta

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config import IMAGES_FOLDER, VPNAPI_KEY, Config, limiter
from error_handlers import register_error_handlers
from middleware import (
    check_headers,
    check_user_agent,
    check_vpn,
    set_csp,
    set_secure_headers,
)
from routes import register_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


@app.before_request
def before_request():
    # Check headers
    response = check_headers()
    if response:
        return response

    # Check User-Agent
    response = check_user_agent()
    if response:
        return response

    # Check VPN, Proxy, Tor Node and Relay
    response = check_vpn()
    if response:
        return response


@app.after_request
def after_request(response):
    # Set content security policy and secure headers
    response = set_csp(response)
    if response:
        return response

    # Set secure headers
    response = set_secure_headers(response)
    if response:
        return response


# Load configuration from Config class
app.config.from_object(Config)

# Set JWT configuration from environment variables
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["IMAGES_FOLDER"] = IMAGES_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # 1 MB

limiter.init_app(app)


@app.route("/")
def home():
    return jsonify(message="Hello there!")


# Register routes and error handlers
register_routes(app)
register_error_handlers(app)

if __name__ == "__main__":
    # Run the app with specified host and port from environment variables
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
