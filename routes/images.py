import os

from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required

from config import IMAGES_FOLDER, limiter
from db import get_db_connection

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
images_blueprint = Blueprint("images", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@images_blueprint.route("", methods=["POST"])
@limiter.limit("2 per minute")
@limiter.limit("10 per day")
@jwt_required()
def upload_image():
    if "file" not in request.files:
        return jsonify(error="No file part in the request"), 400

    file = request.files["file"]
    image_type = request.form.get("image_type")

    if file.filename == "":
        return jsonify(error="No selected file"), 400

    if file and allowed_file(file.filename):
        # Change filename to a random string
        filename = os.urandom(15).hex() + "." + file.filename.rsplit(".", 1)[1].lower()
        path = os.path.join(IMAGES_FOLDER, filename)

        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.callproc("create_image", [path, image_type])
            file.save(path)
            return jsonify(message="File successfully uploaded"), 200
    else:
        return jsonify(message="File type is not allowed"), 400


@images_blueprint.route("/<path:filename>", methods=["GET"])
def get_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)
