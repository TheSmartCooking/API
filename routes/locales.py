from flask import Blueprint, request, jsonify
from db import get_db_connection

locales_blueprint = Blueprint('locales', __name__)

@locales_blueprint.route('/', methods=['GET'])
def get_all_locales():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_all_locales')
        person = cursor.fetchone()
    db.close()

    return jsonify(person)
