from flask import Blueprint, request, jsonify
from db import get_db_connection

statuses_blueprint = Blueprint('statuses', __name__)
