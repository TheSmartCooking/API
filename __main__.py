# __main__.py
from flask import Flask, request, jsonify
import pymysql.cursors

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Route for the `get_paginated_recipes` procedure
@app.route('/recipes', methods=['GET'])
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

# Route for the `get_person_by_id` procedure
@app.route('/person/<int:person_id>', methods=['GET'])
def get_person_by_id(person_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_person_by_id', [person_id])
        person = cursor.fetchone()
    db.close()

    return jsonify(person)

# Route for the `get_recipe_by_id` procedure
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_recipe_by_id', [recipe_id])
        recipe = cursor.fetchone()
    db.close()

    return jsonify(recipe)

# Route for the `get_comments_by_recipe_id` procedure
@app.route('/recipe/<int:recipe_id>/comments', methods=['GET'])
def get_comments_by_recipe_id(recipe_id):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_comments_by_recipe_id', [recipe_id, page, page_size])
        comments = cursor.fetchall()
    db.close()

    return jsonify(comments)

# Route for the `get_paginated_tags` procedure
@app.route('/tags', methods=['GET'])
def get_paginated_tags():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_paginated_tags', [page, page_size])
        tags = cursor.fetchall()
    db.close()

    return jsonify(tags)

# Route for the `get_tags_by_recipe_id` procedure
@app.route('/recipe/<int:recipe_id>/tags', methods=['GET'])
def get_tags_by_recipe_id(recipe_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc('get_tags_by_recipe_id', [recipe_id])
        tags = cursor.fetchall()
    db.close()

    return jsonify(tags)

# TODO: Add the other routes in the same way

if __name__ == '__main__':
    app.run(debug=True)
