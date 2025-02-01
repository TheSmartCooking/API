from argon2 import exceptions
from flask import Blueprint, jsonify, request
from pymysql import MySQLError

from config import limiter

from jwt_helper import (
    TokenError,
    extract_token_from_header,
    generate_access_token,
    generate_refresh_token,
    verify_token,
)
from utility import (
    database_cursor,
    hash_password,
    validate_password,
    verify_password,
)

authentication_blueprint = Blueprint("authentication", __name__)


def login_person_by_email(email):
    with database_cursor() as cursor:
        cursor.callproc("login_person_by_email", (email,))
        return cursor.fetchone()


def update_last_login(person_id):
    with database_cursor() as cursor:
        cursor.callproc("update_last_login", (person_id,))


@authentication_blueprint.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    name = data.get("username")
    email = data.get("email")
    password = data.get("password")
    language_code = data.get("language_code", "en")

    if not name or not email or not password:
        return jsonify(message="Username, email, and password are required"), 400

    if not validate_password(password):
        return jsonify(message="Password does not meet security requirements"), 400

    hashed_password = hash_password(password)

    try:
        with database_cursor() as cursor:
            cursor.callproc(
                "register_person", (name, email, hashed_password, language_code)
            )
    except MySQLError as e:
        if "User name already exists" in str(e):
            return jsonify(message="User name already exists"), 400
        elif "Email already exists" in str(e):
            return jsonify(message="Email already exists"), 400
        else:
            return jsonify(message="An error occurred during registration"), 500

    return jsonify(message="User created successfully"), 201


@authentication_blueprint.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(message="Email and password are required"), 400

    person = login_person_by_email(email)

    if not person:
        return jsonify(message="Invalid credentials"), 401

    try:
        verify_password(password, person["hashed_password"])
    except exceptions.VerifyMismatchError:
        return jsonify(message="Invalid credentials"), 401
    except Exception:
        return jsonify(message="An internal error occurred"), 500

    person_id = person["person_id"]
    access_token = generate_access_token(person_id)
    refresh_token = generate_refresh_token(person_id)
    update_last_login(person_id)

    return jsonify(
        message="Login successful",
        access_token=access_token,
        refresh_token=refresh_token,
    )


@authentication_blueprint.route("/refresh", methods=["POST"])
@limiter.limit("5 per hour")
def refresh_token():
    try:
        token = extract_token_from_header()
        decoded = verify_token(token, required_type="refresh")
        person_id = decoded["person_id"]

        new_access_token = generate_access_token(person_id)
        return jsonify(access_token=new_access_token), 200
    except TokenError as e:
        return jsonify(message=e.message), e.status_code
