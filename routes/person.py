from flask import Blueprint, jsonify

from db import get_db_connection

person_blueprint = Blueprint("person", __name__)


@person_blueprint.route("/all", methods=["GET"])
def get_all_persons():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_persons")
        persons = cursor.fetchall()
    db.close()
    return jsonify(persons)


@person_blueprint.route("/<int:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_person_by_id", (person_id,))
        person = cursor.fetchone()
    db.close()
    return jsonify(person)
