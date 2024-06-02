from flask import Blueprint, jsonify, request

from config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from db import get_db_connection

tags_blueprint = Blueprint("tags", __name__)


@tags_blueprint.route("/", methods=["GET"])
def get_paginated_tags():
    page = int(request.args.get("page", DEFAULT_PAGE))
    page_size = int(request.args.get("page_size", DEFAULT_PAGE_SIZE))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_paginated_tags", [page, page_size])
        tags = cursor.fetchall()
    db.close()

    return jsonify(tags)
