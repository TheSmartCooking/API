from flask import Blueprint, request, jsonify
from db import get_db_connection

locales_blueprint = Blueprint('locales', __name__)
