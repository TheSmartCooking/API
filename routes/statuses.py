from flask import Blueprint, jsonify
from db import get_db_connection

statuses_blueprint = Blueprint('statuses', __name__)

@statuses_blueprint.route('/', methods=['GET'])
def get_all_statuses():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_all_statuses')
        statuses = cursor.fetchall()
    db.close()

    return jsonify(statuses)
