from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from db import get_db_connection

interactions_blueprint = Blueprint("interactions", __name__)


@interactions_blueprint.route("/favorite", methods=["POST"])
@jwt_required()
def favorite_recipe():
    current_user = get_jwt_identity()
    recipe_id = request.args.get("recipe_id")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("create_favorite", (current_user, recipe_id))
        db.commit()
    db.close()

    return jsonify(message="Recipe successfully favorited"), 200


@interactions_blueprint.route("/favorite", methods=["DELETE"])
@jwt_required()
def unfavorite_recipe():
    current_user = get_jwt_identity()
    recipe_id = request.args.get("recipe_id")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("delete_favorite", (current_user, recipe_id))
        db.commit()
    db.close()

    return jsonify(message="Recipe successfully unfavorited"), 200


@interactions_blueprint.route("/rate", methods=["POST"])
@jwt_required()
def rate_recipe():
    current_user = get_jwt_identity()
    recipe_id = request.args.get("recipe_id")
    rating = request.json.get("rating")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("create_recipe_rating", (current_user, recipe_id, rating))
        db.commit()
    db.close()

    return jsonify(message="Recipe successfully rated"), 200


@interactions_blueprint.route("/comment", methods=["POST"])
@jwt_required()
def comment_recipe():
    current_user = get_jwt_identity()
    recipe_id = request.args.get("recipe_id")
    comment = request.json.get("comment")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("create_comment", (current_user, recipe_id, comment))
        db.commit()
    db.close()

    return jsonify(message="Comment successfully created"), 200


@interactions_blueprint.route("/comment", methods=["DELETE"])
@jwt_required()
def delete_comment():
    comment_id = request.args.get("comment_id")

    # TODO: Load the comment first to verify that the user is the author

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("delete_comment", (comment_id,))
        db.commit()
    db.close()

    return jsonify(message="Comment successfully deleted"), 200


@interactions_blueprint.route("/like-comment", methods=["POST"])
@jwt_required()
def like_comment():
    current_user = get_jwt_identity()
    comment_id = request.args.get("comment_id")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("create_comment_like", (current_user, comment_id))
        db.commit()
    db.close()

    return jsonify(message="Comment successfully liked"), 200


@interactions_blueprint.route("/like-comment", methods=["DELETE"])
@jwt_required()
def unlike_comment():
    current_user = get_jwt_identity()
    comment_id = request.args.get("comment_id")

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("delete_comment_like", (current_user, comment_id))
        db.commit()
    db.close()

    return jsonify(message="Comment successfully unliked"), 200
