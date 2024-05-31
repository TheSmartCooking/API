from .recipes import recipes_blueprint
from .persons import persons_blueprint
from .tags import tags_blueprint
from .locales import locales_blueprint
from .statuses import statuses_blueprint

def register_routes(app):
    app.register_blueprint(recipes_blueprint, url_prefix='/recipes')
    app.register_blueprint(persons_blueprint, url_prefix='/persons')
    app.register_blueprint(tags_blueprint, url_prefix='/tags')
    app.register_blueprint(locales_blueprint, url_prefix='/locales')
    app.register_blueprint(statuses_blueprint, url_prefix='/statuses')
