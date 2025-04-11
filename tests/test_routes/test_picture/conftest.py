import pytest
from flask import Flask

from routes.picture import picture_blueprint


@pytest.fixture
def app():
    """Create and configure a new Flask application instance for testing"""
    app = Flask(__name__)
    app.register_blueprint(picture_blueprint)
    return app


@pytest.fixture
def auth_header(sample_access_token):
    return {"Authorization": f"Bearer {sample_access_token}"}
