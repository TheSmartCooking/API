from flask import Blueprint, request, jsonify
from db import get_db_connection

ratings_blueprint = Blueprint('ratings', __name__)
