from flask import Blueprint, request, jsonify
from db import get_db_connection

ingredients_blueprint = Blueprint('ingredients', __name__)
