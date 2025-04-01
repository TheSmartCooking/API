import os

from flask import Blueprint, jsonify, request, send_from_directory

from config import Config
from jwt_helper import token_required
from utility import database_cursor

picture_blueprint = Blueprint("picture", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_file_extension(filename):
    return filename.rsplit(".", 1)[1].lower()


@picture_blueprint.route("/all", methods=["GET"])
def get_all_pictures():
    picture_type = request.args.get("type", None)

    with database_cursor() as cursor:
        if picture_type is not None:
            cursor.callproc("get_pictures_by_type", (picture_type,))
        else:
            cursor.callproc("get_all_pictures")
        pictures = cursor.fetchall()
    return jsonify(pictures)


@picture_blueprint.route("/<int:picture_id>", methods=["GET"])
def get_picture_by_id(picture_id):
    with database_cursor() as cursor:
        cursor.callproc("get_picture_by_id", (picture_id,))
        picture = cursor.fetchone()
    return jsonify(picture)


@picture_blueprint.route("/author/<int:author_id>", methods=["GET"])
def get_pictures_by_author(author_id):
    with database_cursor() as cursor:
        cursor.callproc("get_pictures_by_author", (author_id,))
        picture = cursor.fetchall()
    return jsonify(picture)


@picture_blueprint.route("/<path:filename>", methods=["GET"])
def get_picture(filename):
    return send_from_directory(Config.IMAGES_FOLDER, filename)


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
            procedure = "insert_picture_recipe_picture"
        case "avatar":
            procedure = "insert_picture_avatar"
        case "language_icon":
            procedure = "insert_picture_language_icon"
        case _:
            return jsonify({"error": f"Invalid picture type: {picture_type}"}), 400

    with database_cursor() as cursor:
        cursor.callproc(procedure, (hexname, request.person_id))

    fullpath = os.path.abspath(os.path.join(Config.IMAGES_FOLDER, hexname))
    if os.path.commonpath([fullpath, Config.IMAGES_FOLDER]) != Config.IMAGES_FOLDER:
        return jsonify({"error": "Invalid file path"}), 400
    file.save(fullpath)

    return jsonify({"picture_path": hexname}), 201
