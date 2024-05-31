from flask import Blueprint, request, jsonify
from db import get_db_connection

locales_blueprint = Blueprint('locales', __name__)

@locales_blueprint.route('/<int:person_id>', methods=['GET'])
