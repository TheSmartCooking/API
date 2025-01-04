import os
from re import match

from argon2 import PasswordHasher, exceptions
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from pymysql import MySQLError

from db import database_cursor
from jwt_helper import (
    TokenError,
    extract_token_from_header,
    generate_access_token,
    generate_refresh_token,
    verify_token,
)

load_dotenv()

authentication_blueprint = Blueprint("authentication", __name__)
ph = PasswordHasher()
PEPPER = os.getenv("PEPPER", "SuperSecretPepper").encode("utf-8")


def hash_password_with_salt_and_pepper(password: str) -> tuple[str, bytes]:
    salt = os.urandom(16)
    seasoned_password = password.encode("utf-8") + salt + PEPPER
    return ph.hash(seasoned_password), salt


def validate_password(password):
    """
    Validates a password based on the following criteria:
    - At least 12 characters long.
    - Contains at least one uppercase letter (A-Z).
    - Contains at least one lowercase letter (a-z).
    - Contains at least one digit (0-9).
    - Contains at least one special character (any non-alphanumeric character).
    """
    return bool(
        match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$", password)
    )


def get_person_by_email(email):
    with database_cursor() as cursor:
        cursor.callproc("login_person", (email,))
        return cursor.fetchone()


def verify_password(password, stored_password, salt):
    seasoned_password = password.encode("utf-8") + salt + PEPPER
    try:
        return ph.verify(stored_password, seasoned_password)
    except exceptions.VerifyMismatchError:
        return False


def update_last_login(person_id):
    with database_cursor() as cursor:
        cursor.callproc("update_last_login", (person_id,))


@authentication_blueprint.route("/register", methods=["POST"])
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

    hashed_password, salt = hash_password_with_salt_and_pepper(password)

    try:
        with database_cursor() as cursor:
            cursor.callproc(
                "register_person", (name, email, hashed_password, salt, language_code)
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
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(message="Email and password are required"), 400

    person = get_person_by_email(email)

    try:
        if not person or not verify_password(
            password, person["hashed_password"], person["salt"]
        ):
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
def refresh_token():
    try:
        token = extract_token_from_header()
        decoded = verify_token(token, required_type="refresh")
        person_id = decoded["person_id"]

        new_access_token = generate_access_token(person_id)
        return jsonify(access_token=new_access_token), 200
    except TokenError as e:
        return jsonify(message=e.message), e.status_code
