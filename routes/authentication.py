import os
from re import match

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from pymysql import MySQLError

from db import get_db_connection

load_dotenv()

authentications_blueprint = Blueprint("authentications", __name__)
ph = PasswordHasher()


def hash_password_with_salt_and_pepper(password: str, salt: bytes) -> str:
    pepper = os.getenv("PEPPER", "SuperSecretPepper").encode("utf-8")
    password_with_pepper = pepper + salt + password.encode("utf-8")
    hash = ph.hash(password_with_pepper)
    return hash


def validate_password(password):
    return bool(
        match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$", password)
    )


@authentications_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    locale_code = data.get("locale_code", "en")

    if not username or not email or not password:
        return jsonify(message="Username, email, and password are required"), 400

    if not validate_password(password):
        return jsonify(message="Password does not meet security requirements"), 400

    salt = os.urandom(16)
    hashed_password = hash_password_with_salt_and_pepper(password, salt)

    db = get_db_connection()
    with db.cursor() as cursor:
        try:
            cursor.callproc(
                "register_person", (username, email, hashed_password, salt, locale_code)
            )
            db.commit()
        except MySQLError as e:
            if e.args[0] == 1644:
                return jsonify(message="Email already in use"), 400
            else:
                return jsonify(message="An error occurred during registration"), 500

    return jsonify(message="User created successfully"), 201


@authentications_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(message="Email and password are required"), 400

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT person_id, password, salt FROM person WHERE email = %s", (email,)
        )
        user = cursor.fetchone()

        if user:
            cursor.callproc("update_last_login", (user["person_id"],))
            db.commit()

            stored_password = user["password"]
            salt = user["salt"]
            pepper = os.getenv("PEPPER", "SuperSecretPepper").encode("utf-8")
            password_with_pepper = pepper + salt + password.encode("utf-8")

            try:
                ph.verify(stored_password, password_with_pepper)
                access_token = create_access_token(
                    identity=user["person_id"], fresh=True
                )
                refresh_token = create_refresh_token(identity=user["person_id"])
                return (
                    jsonify(access_token=access_token, refresh_token=refresh_token),
                    200,
                )
            except VerifyMismatchError:
                pass

    return jsonify(message="Invalid credentials"), 401


@authentications_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("update_last_login", (current_user,))
        db.commit()
    db.close()
    new_access_token = create_access_token(identity=current_user, fresh=False)
    return jsonify(access_token=new_access_token), 200
