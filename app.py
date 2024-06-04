import os
from datetime import timedelta

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config import IMAGES_FOLDER, VPNAPI_KEY, Config, limiter
from error_handlers import register_error_handlers
from routes import register_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Prevent VPNs and proxies from accessing the API
@app.before_request
def before_request():
    data = requests.get(
        f"https://vpnapi.io/api/{request.remote_addr}?key={VPNAPI_KEY}"
    ).json()

    # If the IP is a VPN, return a 403 Forbidden response
    if "security" in data and any(data["security"].values()):
        return jsonify(message="You are not allowed to access this resource"), 403


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
