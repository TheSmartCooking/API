from flask import Blueprint, jsonify, request

from utils import database_cursor

recipe_engagement_blueprint = Blueprint("recipe_engagement", __name__)


@recipe_engagement_blueprint.route("/all", methods=["GET"])
def get_all_recipe_engagements():
    engagement_type = request.args.get("type", None)

    if engagement_type and engagement_type not in ["like", "favorite", "view"]:
        return jsonify({"error": "Invalid engagement type"}), 400

    with database_cursor() as cursor:
        if engagement_type:
            cursor.callproc("get_all_engagements_by_type", (engagement_type,))
        else:
            cursor.callproc("get_all_recipe_engagements")
        recipe_engagements = cursor.fetchall()
    return jsonify(recipe_engagements)
