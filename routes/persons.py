from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

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
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipes_by_author", [person_id])
        recipes = cursor.fetchall()
    db.close()

    return jsonify(recipes)


@persons_blueprint.route("/<int:person_id>/comments", methods=["GET"])
def get_comments_by_person(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_comments_by_person", [person_id])
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
