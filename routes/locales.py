from flask import Blueprint, jsonify

from db import get_db_connection

locales_blueprint = Blueprint("locales", __name__)


@locales_blueprint.route("/codes", methods=["GET"])
def get_locales_codes():
    db = get_db_connection()
    with db.cursor() as cursor:
        # Call the stored procedure
        cursor.callproc("get_locales_codes")
        locales = cursor.fetchone()
    db.close()

    return jsonify(locales["locale_codes"].split(","))


@locales_blueprint.route("/list", methods=["GET"])
def get_all_locales():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_locales")
        locales = cursor.fetchall()
    db.close()

    return jsonify(locales)
