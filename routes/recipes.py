from flask import Blueprint, jsonify, request

from config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from db import get_db_connection

recipes_blueprint = Blueprint("recipes", __name__)


@recipes_blueprint.route("/list", methods=["GET"])
def get_paginated_recipes():
    locale_code = request.args.get("locale_code", "en_US")
    status_name = request.args.get("status_name", "published")
    page = int(request.args.get("page", DEFAULT_PAGE))
    page_size = int(request.args.get("page_size", DEFAULT_PAGE_SIZE))
    sort_order = request.args.get("sort_order", "most_popular")
    tags = request.args.get("tags", None)

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc(
            "get_paginated_recipes",
            [locale_code, status_name, page, page_size, sort_order, tags],
        )

        recipes = cursor.fetchall()
    db.close()

    return jsonify(recipes)


@recipes_blueprint.route("/<int:recipe_id>", methods=["GET"])
def get_recipe_by_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_by_id", [recipe_id])
        recipe = cursor.fetchone()
    db.close()

    return jsonify(recipe)


@recipes_blueprint.route("/<int:recipe_id>/tags", methods=["GET"])
def get_tags_by_recipe_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_tags_by_recipe_id", [recipe_id])
        tags = cursor.fetchall()
    db.close()

    return jsonify(tags)


@recipes_blueprint.route("/<int:recipe_id>/ingredients", methods=["GET"])
def get_recipe_ingredients_by_recipe_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_ingredients_by_recipe_id", [recipe_id])
        ingredients = cursor.fetchall()
    db.close()

    return jsonify(ingredients)


@recipes_blueprint.route("/<int:recipe_id>/comments", methods=["GET"])
def get_comments_by_recipe_id(recipe_id):
    page = int(request.args.get("page", DEFAULT_PAGE))
    page_size = int(request.args.get("page_size", DEFAULT_PAGE_SIZE))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_comments_by_recipe_id", [recipe_id, page, page_size])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)


@recipes_blueprint.route("/<int:recipe_id>/translations", methods=["GET"])
def get_recipe_translations_by_recipe_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_translations_by_recipe_id", [recipe_id])
        translations = cursor.fetchall()
    db.close()

    return jsonify(translations)


@recipes_blueprint.route("/<int:recipe_id>/ratings", methods=["GET"])
def get_ratings_by_recipe_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_ratings_by_recipe_id", [recipe_id])
        ratings = cursor.fetchall()
    db.close()

    return jsonify(ratings)
