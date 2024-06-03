import os

from flask import Blueprint, jsonify, request

from config import IMAGES_FOLDER
from db import get_db_connection

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
uploads_blueprint = Blueprint("uploads", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads_blueprint.route("/image", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify(error="No file part in the request"), 400

    file = request.files["file"]
    image_type = request.form.get("image_type")

    if file.filename == "":
        return jsonify(error="No selected file"), 400

    if file and allowed_file(file.filename):
        # Change filename to a random string
        filename = os.urandom(15).hex() + file.filename.rsplit(".", 1)[1].lower()
        path = os.path.join(IMAGES_FOLDER, filename)

        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.callproc("create_image", [path, image_type])
            file.save(path)
            return jsonify(message="File successfully uploaded"), 200
    else:
        return jsonify(message="File type is not allowed"), 400
