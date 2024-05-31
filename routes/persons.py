from flask import Blueprint, request, jsonify
from db import get_db_connection

persons_blueprint = Blueprint('persons', __name__)

@persons_blueprint.route('/<int:person_id>', methods=['GET'])
def get_person_by_id(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_person_by_id', [person_id])
        person = cursor.fetchone()
    db.close()

    return jsonify(person)
