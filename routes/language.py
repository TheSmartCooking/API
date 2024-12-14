from flask import Blueprint, jsonify

from db import get_db_connection

language_blueprint = Blueprint("language", __name__)


@language_blueprint.route("/all", methods=["GET"])
def get_all_languages():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_languages")
        languages = cursor.fetchall()
    db.close()
    return jsonify(languages)


@language_blueprint.route("/<int:language_id>", methods=["GET"])
def get_language_by_id(language_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_language_by_id", (language_id,))
        language = cursor.fetchone()
    db.close()
    return jsonify(language)


@language_blueprint.route("/<string:language_code>", methods=["GET"])
def get_language_by_language_code(language_code):
    if len(language_code) != 2:
        return jsonify({"error": "Invalid language code"}), 400

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_language_by_code", (language_code,))
        language = cursor.fetchone()
    db.close()
    return jsonify(language)


@language_blueprint.route("/used", methods=["GET"])
def get_used_languages():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_languages_with_users")
        languages = cursor.fetchall()
    db.close()
    return jsonify(languages)


@language_blueprint.route("/stats", methods=["GET"])
def get_language_stats():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_languages_usage_statistics")
        stats = cursor.fetchall()
    db.close()
    return jsonify(stats)
