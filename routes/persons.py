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

@persons_blueprint.route('/<int:person_id>/recipes', methods=['GET'])
def get_recipes_by_author(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_recipes_by_author', [person_id])
        recipes = cursor.fetchall()
    db.close()

    return jsonify(recipes)

@persons_blueprint.route('/<int:person_id>/comments', methods=['GET'])
def get_comments_by_person(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_comments_by_person', [person_id])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)

@persons_blueprint.route('/<int:person_id>/favorites', methods=['GET'])
def get_favorites_by_person_id(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_favorites_by_person_id', [person_id])
        favorites = cursor.fetchall()
    db.close()

    return jsonify(favorites)
