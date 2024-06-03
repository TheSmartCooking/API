from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

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
def get_comments_by_person(person_id):
    page = int(request.args.get("page", DEFAULT_PAGE))
    page_size = int(request.args.get("page_size", DEFAULT_PAGE_SIZE))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_comments_by_person", [person_id, page, page_size])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)


@persons_blueprint.route("/<int:person_id>/favorites", methods=["GET"])
@jwt_required
def get_favorites_by_person_id(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_favorites_by_person_id", [person_id])
        favorites = cursor.fetchall()
    db.close()

    return jsonify(favorites)
