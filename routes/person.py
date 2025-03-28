from argon2 import exceptions
from flask import Blueprint, jsonify, request

from utility import *

person_blueprint = Blueprint("person", __name__)


def login_person_by_id(person_id: int) -> dict:
    with database_cursor() as cursor:
        cursor.callproc("login_person_by_id", (person_id,))
        return cursor.fetchone()


def mask_person_email(person: dict) -> None:
    """Mask the email address of a person safely."""
    encrypted_email = person.get("encrypted_email")

    if not encrypted_email:
        person["email"] = "Unknown"
        return

    try:
        person["email"] = mask_email(decrypt_email(encrypted_email))
    except Exception:
        person["email"] = "Decryption Error"

    # Remove unreadable fields
    person.pop("encrypted_email", None)
    person.pop("hashed_password", None)


def update_person_in_db(person_id, name, email, hashed_password, locale_code):
    email = hash_email(email), encrypt_email(email)

    with database_cursor() as cursor:
        cursor.callproc(
            "update_person",
            (person_id, name, *email, hashed_password, locale_code),
        )


@person_blueprint.route("/all", methods=["GET"])
def get_all_persons():
    with database_cursor() as cursor:
        cursor.callproc("get_all_persons")
        persons = cursor.fetchall()

    for person in persons:
        mask_person_email(person)

    return jsonify(persons)


@person_blueprint.route("/<int:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    with database_cursor() as cursor:
        cursor.callproc("get_person_by_id", (person_id,))
        person = cursor.fetchone()

    mask_person_email(person)
    return jsonify(person)


@person_blueprint.route("/<int:person_id>", methods=["PUT", "PATCH"])
def update_person(person_id):
    data = request.get_json()
    name = data.get("username", None)
    email = data.get("email", None)
    current_password = data.get("current_password")
    new_password = data.get("new_password", None)
    locale_code = data.get("locale_code", None)

    if new_password and not validate_password(new_password):
        return jsonify(message="Password does not meet security requirements"), 400

    hashed_password = None
    if new_password:
        person = login_person_by_id(person_id)
        if not person:
            return jsonify(message="Invalid credentials"), 401

        try:
            verify_password(current_password, person["hashed_password"])
        except exceptions.VerifyMismatchError:
            return jsonify(message="Invalid credentials"), 401
        except Exception:
            return jsonify(message="An unknown error occurred"), 500

        hashed_password = hash_password(new_password)

    update_person_in_db(person_id, name, email, hashed_password, locale_code)
    return jsonify(message="Person updated successfully"), 200
