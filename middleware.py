# middleware.py

import requests
from flask import jsonify, request

VPNAPI_KEY = "your_vpnapi_key"


def check_user_agent():
    user_agent = request.headers.get("User-Agent")
    if (
        not user_agent
        or "curl" in user_agent.lower()
        or "python-requests" in user_agent.lower()
    ):
        return jsonify(message="Suspicious User-Agent"), 403


def check_vpn():
    data = requests.get(
        f"https://vpnapi.io/api/{request.remote_addr}?key={VPNAPI_KEY}"
    ).json()

    if "security" in data and any(data["security"].values()):
        return jsonify(message="You are not allowed to access this resource"), 403


def set_csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


def set_secure_headers(response):
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
