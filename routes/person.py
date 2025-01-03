from flask import Blueprint, jsonify

from db import database_cursor

person_blueprint = Blueprint("person", __name__)


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
