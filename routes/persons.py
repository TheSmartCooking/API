from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from db import get_db_connection

persons_blueprint = Blueprint("persons", __name__)


@persons_blueprint.route("/<int:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_person_by_id", [person_id])
        person = cursor.fetchone()
    db.close()

    return jsonify(person)


@persons_blueprint.route("/<int:person_id>/recipes", methods=["GET"])
def get_recipes_by_author(person_id):
    page = int(request.args.get("page", DEFAULT_PAGE))
    page_size = int(request.args.get("page_size", DEFAULT_PAGE_SIZE))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipes_by_author", [person_id, page, page_size])
        recipes = cursor.fetchall()
    db.close()

    return jsonify(recipes)


@persons_blueprint.route("/<int:person_id>/comments", methods=["GET"])
@jwt_required()
def get_comments_by_person(person_id):
    current_user = get_jwt_identity()

    if current_user != person_id:
        return jsonify(message="Unauthorized"), 401

    page = int(request.args.get("page", DEFAULT_PAGE))
    page_size = int(request.args.get("page_size", DEFAULT_PAGE_SIZE))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_comments_by_person", [person_id, page, page_size])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)


@persons_blueprint.route("/<int:person_id>/favorites", methods=["GET"])
@jwt_required()
def get_favorites_by_person_id(person_id):
    current_user = get_jwt_identity()

    if current_user != person_id:
        return jsonify(message="Unauthorized"), 401

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_favorites_by_person_id", [person_id])
        favorites = cursor.fetchall()
    db.close()

    return jsonify(favorites)


@persons_blueprint.route("/<int:person_id>/locale", methods=["POST"])
@jwt_required()
def update_person_locale(person_id):
    current_user = get_jwt_identity()

    if current_user != person_id:
        return jsonify(message="Unauthorized"), 401

    data = request.get_json()
    locale_code = data.get("locale_code")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("update_person_locale", [person_id, locale_code])
        db.commit()
    db.close()

    return jsonify(message="Locale updated successfully")
