from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from pymysql import MySQLError
from db import get_db_connection
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os

load_dotenv()

authentications_blueprint = Blueprint('authentications', __name__)
ph = PasswordHasher()

def hash_password_with_salt_and_pepper(password: str, salt: bytes) -> tuple:
    pepper = os.getenv('PEPPER').encode('utf-8')
    password_with_pepper = pepper + password.encode('utf-8')
    hash = ph.hash(password_with_pepper)
    return hash, salt

@authentications_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400

    hashed_password, salt = hash_password_with_salt_and_pepper(password, os.urandom(16))

    db = get_db_connection()
    with db.cursor() as cursor:
        try:
            cursor.callproc('create_person', (username, email, hashed_password, salt))
            db.commit()
        except MySQLError as e:
            if e.args[0] == 1062:  # Error number for 'Duplicate entry'
                return jsonify({"message": "Email already in use"}), 400
            else:
                return jsonify({"message": "An error occurred during registration"}), 500

    return jsonify({"message": "User created successfully"}), 201


@authentications_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute('SELECT password, salt FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            entered_password = hash_password_with_salt_and_pepper(user['password'], user['salt'])

            try:
                ph.verify(user['password'], entered_password)
                access_token = create_access_token(identity={'username': username})
                return jsonify(access_token=access_token), 200
            except VerifyMismatchError:
                pass

    return jsonify({"message": "Invalid credentials"}), 401

@authentications_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
