from .authentication import authentications_blueprint
from .locales import locales_blueprint
from .persons import persons_blueprint
from .recipes import recipes_blueprint
from .statuses import statuses_blueprint
from .tags import tags_blueprint


def register_routes(app):
    app.register_blueprint(authentications_blueprint, url_prefix="/authentication")
    app.register_blueprint(recipes_blueprint, url_prefix="/recipe")
    app.register_blueprint(persons_blueprint, url_prefix="/person")
    app.register_blueprint(tags_blueprint, url_prefix="/tag")
    app.register_blueprint(locales_blueprint, url_prefix="/locale")
    app.register_blueprint(statuses_blueprint, url_prefix="/status")
