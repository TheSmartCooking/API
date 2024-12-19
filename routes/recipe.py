from flask import Blueprint, jsonify, request

from config import DEFAULT_PAGE_SIZE
from db import get_db_connection

recipe_blueprint = Blueprint("recipe", __name__)


@recipe_blueprint.route("/all", methods=["GET"])
def get_all_recipes():
    offset = max(1, request.args.get("page", 1, type=int))
    limit = max(1, request.args.get("page_size", DEFAULT_PAGE_SIZE, type=int))
    language_code = request.args.get("language_code", "en")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_recipes_paginated", (limit, offset, language_code))
        recipes = cursor.fetchall()
    db.close()
    return jsonify(recipes)


@recipe_blueprint.route("/<int:recipe_id>", methods=["GET"])
def get_recipe_by_id(recipe_id):
    language_code = request.args.get("language_code", "en")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_by_id", (recipe_id, language_code))
        recipe = cursor.fetchone()
    db.close()
    return jsonify(recipe)


@recipe_blueprint.route("/<int:recipe_id>/engagements", methods=["GET"])
def get_recipe_engagement(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_engagement", (recipe_id,))
        engagement = cursor.fetchone()
    db.close()
    return jsonify(engagement)


@recipe_blueprint.route("/<int:recipe_id>/ingredients", methods=["GET"])
def get_recipe_ingredients(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_ingredients", (recipe_id,))
        ingredients = cursor.fetchall()
    db.close()
    return jsonify(ingredients)


@recipe_blueprint.route("/<int:recipe_id>/tags", methods=["GET"])
def get_recipe_tags(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_recipe_tags", (recipe_id,))
        tags = cursor.fetchall()
    db.close()
    return jsonify(tags)
