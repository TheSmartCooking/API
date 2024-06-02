import os
from re import match

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from pymysql import MySQLError

from db import get_db_connection

load_dotenv()

authentications_blueprint = Blueprint("authentications", __name__)
ph = PasswordHasher()


def hash_password_with_salt_and_pepper(password: str, salt: bytes) -> str:
    pepper = os.getenv("PEPPER")
    password_with_pepper = pepper.encode("utf-8") + salt + password.encode("utf-8")
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

    if not username or not email or not password:
        return jsonify(message="Username, email, and password are required"), 400

    if not validate_password(password):
        return jsonify(message="Password does not meet security requirements"), 400

    salt = os.urandom(16)
    hashed_password = hash_password_with_salt_and_pepper(password, salt)

    db = get_db_connection()
    with db.cursor() as cursor:
        try:
            cursor.callproc("create_person", (username, email, hashed_password, salt))
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
        cursor.execute("SELECT password, salt FROM person WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            stored_password = user["password"]
            salt = user["salt"]
            pepper = os.getenv("PEPPER").encode("utf-8")
            password_with_pepper = pepper + salt + password.encode("utf-8")

            try:
                ph.verify(stored_password, password_with_pepper)
                access_token = create_access_token(identity={"username": email})
                return jsonify(access_token=access_token), 200
            except VerifyMismatchError:
                pass

    return jsonify(message="Invalid credentials"), 401


@authentications_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
