import os

from flask import Blueprint, jsonify, request, send_from_directory

from config import PICTURE_FOLDER
from db import get_db_connection
from jwt_helper import token_required

picture_blueprint = Blueprint("picture", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_file_extension(filename):
    return filename.rsplit(".", 1)[1].lower()


@picture_blueprint.route("/<path:filename>", methods=["GET"])
def get_picture(filename):
    return send_from_directory(PICTURE_FOLDER, filename)


@picture_blueprint.route("", methods=["POST"])
@token_required
def upload_picture():
    if not request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    picture_type = request.form.get("type")

    if not is_allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    hexname = os.urandom(30).hex() + "." + extract_file_extension(file.filename)

    match picture_type:
        case "recipe":
            procedure = "insert_recipe_picture"
        case "avatar":
            procedure = "insert_avatar"
        case "language_icon":
            procedure = "insert_language_icon"
        case _:
            return jsonify({"error": f"Invalid picture type: {picture_type}"}), 400

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc(procedure, (hexname, request.person_id))
    db.close()

    file.save(os.path.join(PICTURE_FOLDER, hexname))

    return jsonify({"picture_path": hexname}), 201
