from flask import Blueprint, request, jsonify
from db import get_db_connection

tags_blueprint = Blueprint('tags', __name__)
