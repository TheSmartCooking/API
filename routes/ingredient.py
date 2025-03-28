from flask import Blueprint, jsonify

from utility import database_cursor

ingredient_blueprint = Blueprint("ingredient", __name__)


@ingredient_blueprint.route("/all", methods=["GET"])
def get_all_ingredients():
    with database_cursor() as cursor:
        cursor.callproc("get_all_ingredients")
        ingredients = cursor.fetchall()
    return jsonify(ingredients)


@ingredient_blueprint.route("/<int:ingredient_id>", methods=["GET"])
def get_ingredient_by_id(ingredient_id):
    with database_cursor() as cursor:
        cursor.callproc("get_ingredient_by_id", (ingredient_id,))
        ingredient = cursor.fetchone()
    return jsonify(ingredient)
