from flask import Blueprint, request, jsonify
from db import get_db_connection
from config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE

comments_blueprint = Blueprint('comments', __name__)

@comments_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_comments_by_recipe_id(recipe_id):
    page = int(request.args.get('page', DEFAULT_PAGE))
    page_size = int(request.args.get('page_size', DEFAULT_PAGE_SIZE))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_comments_by_recipe_id', [recipe_id, page, page_size])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)
