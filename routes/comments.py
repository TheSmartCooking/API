from flask import Blueprint, request, jsonify
from db import get_db_connection

comments_blueprint = Blueprint('comments', __name__)

@comments_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_comments_by_recipe_id(recipe_id):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_comments_by_recipe_id', [recipe_id, page, page_size])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)
