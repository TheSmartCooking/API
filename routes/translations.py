from flask import Blueprint, request, jsonify
from db import get_db_connection

translations_blueprint = Blueprint('translations', __name__)
