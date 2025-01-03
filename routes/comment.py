from flask import Blueprint, jsonify

from db import database_cursor, get_db_connection

comment_blueprint = Blueprint("comment", __name__)


@comment_blueprint.route("/all", methods=["GET"])
def get_all_comments():
    with database_cursor() as cursor:
        cursor.callproc("get_all_comments")
        comments = cursor.fetchall()
    return jsonify(comments)


@comment_blueprint.route("/<int:comment_id>", methods=["GET"])
def get_comment_by_id(comment_id):
    with database_cursor() as cursor:
        cursor.callproc("get_comment_by_id", (comment_id,))
        comment = cursor.fetchone()
    return jsonify(comment)


@comment_blueprint.route("/person/<int:person_id>", methods=["GET"])
def get_comments_by_person(person_id):
    with database_cursor() as cursor:
        cursor.callproc("get_all_comments_by_person", (person_id,))
        comments = cursor.fetchall()
    return jsonify(comments)


@comment_blueprint.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_comments_by_recipe(recipe_id):
    with database_cursor() as cursor:
        cursor.callproc("get_all_comments_by_recipe", (recipe_id,))
        comments = cursor.fetchall()
    return jsonify(comments)


@comment_blueprint.route("/count/recipe/<int:recipe_id>", methods=["GET"])
def get_comment_count_by_recipe(recipe_id):
    with database_cursor() as cursor:
        cursor.callproc("get_comment_count_by_recipe", (recipe_id,))
        count = cursor.fetchone()
    return jsonify(count)
