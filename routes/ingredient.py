from flask import Blueprint, jsonify

from db import get_db_connection

ingredient_blueprint = Blueprint("ingredient", __name__)


@ingredient_blueprint.route("/all", methods=["GET"])
def get_all_ingredients():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_ingredients")
        ingredients = cursor.fetchall()
    db.close()
    return jsonify(ingredients)


@ingredient_blueprint.route("/<int:ingredient_id>", methods=["GET"])
def get_ingredient_by_id(ingredient_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_ingredient_by_id", (ingredient_id,))
        ingredient = cursor.fetchone()
    db.close()
    return jsonify(ingredient)
