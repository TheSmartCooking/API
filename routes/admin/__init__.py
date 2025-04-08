from flask import Blueprint

from routes.admin.jwt_rotation import jwt_rotation_blueprint

admin_blueprint = Blueprint("admin", __name__)

admin_blueprint.register_blueprint(jwt_rotation_blueprint, url_prefix="/jwt_keys")
