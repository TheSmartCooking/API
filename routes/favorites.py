from flask import Blueprint, request, jsonify
from db import get_db_connection

favorites_blueprint = Blueprint('favorites', __name__)
