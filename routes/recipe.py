from flask import Blueprint, jsonify, request

from config import DEFAULT_PAGE_SIZE
from utility import database_cursor

recipe_blueprint = Blueprint("recipe", __name__)


@recipe_blueprint.route("/all", methods=["GET"])
def get_all_recipes():
    offset = max(1, request.args.get("page", 1, type=int))
    limit = max(1, request.args.get("page_size", DEFAULT_PAGE_SIZE, type=int))
    language_code = request.args.get("language_code", "en")

    with database_cursor() as cursor:
        cursor.callproc("get_all_recipes_paginated", (limit, offset, language_code))
        recipes = cursor.fetchall()
    return jsonify(recipes)


@recipe_blueprint.route("/search", methods=["GET"])
def get_recipes_by_name():
    name = request.args.get("name")
    offset = max(1, request.args.get("page", 1, type=int))
    limit = max(1, request.args.get("page_size", DEFAULT_PAGE_SIZE, type=int))
    language_code = request.args.get("language_code", "en")

    if not name:
        return jsonify(message="Name is required"), 400

    with database_cursor() as cursor:
        cursor.callproc(
            "get_recipes_by_name_paginated", (name, limit, offset, language_code)
        )
        recipes = cursor.fetchall()
    return jsonify(recipes)


@recipe_blueprint.route("/<int:recipe_id>", methods=["GET"])
def get_recipe_by_id(recipe_id):
    language_code = request.args.get("language_code", "en")

    with database_cursor() as cursor:
        cursor.callproc("get_recipe_by_id", (recipe_id, language_code))
        recipe = cursor.fetchone()
    return jsonify(recipe)


@recipe_blueprint.route("/<int:recipe_id>/engagements", methods=["GET"])
def get_recipe_engagement(recipe_id):
    with database_cursor() as cursor:
        cursor.callproc("get_recipe_engagement", (recipe_id,))
        engagement = cursor.fetchone()
    return jsonify(engagement)


@recipe_blueprint.route("/<int:recipe_id>/ingredients", methods=["GET"])
def get_recipe_ingredients(recipe_id):
    with database_cursor() as cursor:
        cursor.callproc("get_recipe_ingredients", (recipe_id,))
        ingredients = cursor.fetchall()
    return jsonify(ingredients)


@recipe_blueprint.route("/<int:recipe_id>/tags", methods=["GET"])
def get_recipe_tags(recipe_id):
    with database_cursor() as cursor:
        cursor.callproc("get_recipe_tags", (recipe_id,))
        tags = cursor.fetchall()
    return jsonify(tags)


@recipe_blueprint.route("", methods=["POST"])
def add_recipe():
    data = request.json

    # Extract recipe data
    author_id = data.get("author_id")
    picture_id = data.get("picture_id", None)
    cook_time = data.get("cook_time")
    difficulty_level = data.get("difficulty_level", None)
    recipe_source = data.get("recipe_source", None)
    recipe_status = data.get("recipe_status", "draft")

    # Extract translation data
    language_iso_code = data.get("language_iso_code")
    title = data.get("title")
    details = data.get("details")
    preparation = data.get("preparation")
    nutritional_information = data.get("nutritional_information", None)
    video_url = data.get("video_url", None)

    if not all([author_id, cook_time, language_iso_code, title, details, preparation]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        with database_cursor() as cursor:
            cursor.callproc(
                "insert_recipe",
                (
                    author_id,
                    picture_id,
                    cook_time,
                    difficulty_level,
                    recipe_source,
                    recipe_status,
                ),
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            recipe_id = list(cursor.fetchone().values())[0]

            cursor.callproc(
                "insert_recipe_translation_by_iso_code",
                (
                    recipe_id,
                    language_iso_code,
                    title,
                    details,
                    preparation,
                    nutritional_information,
                    video_url,
                ),
            )

            return jsonify({"message": "Recipe added successfully"}), 201

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
