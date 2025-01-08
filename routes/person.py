from flask import Blueprint, jsonify, request

from utility import (
    database_cursor,
    hash_password_with_salt_and_pepper,
    validate_password,
    verify_password,
)

person_blueprint = Blueprint("person", __name__)


def login_person_by_id(person_id):
    with database_cursor() as cursor:
        cursor.callproc("login_person_by_id", (person_id,))
        return cursor.fetchone()


def update_person_in_db(person_id, name, email, hashed_password, salt, locale_code):
    with database_cursor() as cursor:
        cursor.callproc(
            "update_person",
            (person_id, name, email, hashed_password, salt, locale_code),
        )


@person_blueprint.route("/all", methods=["GET"])
def get_all_persons():
    with database_cursor() as cursor:
        cursor.callproc("get_all_persons")
        persons = cursor.fetchall()
    return jsonify(persons)


@person_blueprint.route("/<int:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    with database_cursor() as cursor:
        cursor.callproc("get_person_by_id", (person_id,))
        person = cursor.fetchone()
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

    hashed_password, salt = None, None
    if new_password:
        person = login_person_by_id(person_id)
        if not person or not verify_password(
            current_password, person["hashed_password"], person["salt"]
        ):
            return jsonify(message="Invalid credentials"), 401

        hashed_password, salt = hash_password_with_salt_and_pepper(new_password)

    update_person_in_db(person_id, name, email, hashed_password, salt, locale_code)
    return jsonify(message="Person updated successfully"), 200
