from flask import Blueprint, request, jsonify
from db import get_db_connection

recipes_blueprint = Blueprint('recipes', __name__)

@recipes_blueprint.route('/', methods=['GET'])
def get_paginated_recipes():
    locale_code = request.args.get('locale_code')
    status_name = request.args.get('status_name')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_paginated_recipes', [locale_code, status_name, page, page_size])
        recipes = cursor.fetchall()
    db.close()

    return jsonify(recipes)

@recipes_blueprint.route('/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_recipe_by_id', [recipe_id])
        recipe = cursor.fetchone()
    db.close()

    return jsonify(recipe)
