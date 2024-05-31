from .recipes import recipes_blueprint
from .persons import persons_blueprint
from .comments import comments_blueprint
from .tags import tags_blueprint
from .ingredients import ingredients_blueprint
from .translations import translations_blueprint
from .favorites import favorites_blueprint
from .ratings import ratings_blueprint
from .locales import locales_blueprint
from .statuses import statuses_blueprint

def register_routes(app):
    app.register_blueprint(recipes_blueprint, url_prefix='/recipes')
    app.register_blueprint(persons_blueprint, url_prefix='/persons')
    app.register_blueprint(comments_blueprint, url_prefix='/comments')
    app.register_blueprint(tags_blueprint, url_prefix='/tags')
    app.register_blueprint(ingredients_blueprint, url_prefix='/ingredients')
    app.register_blueprint(translations_blueprint, url_prefix='/translations')
    app.register_blueprint(favorites_blueprint, url_prefix='/favorites')
    app.register_blueprint(ratings_blueprint, url_prefix='/ratings')
    app.register_blueprint(locales_blueprint, url_prefix='/locales')
    app.register_blueprint(statuses_blueprint, url_prefix='/statuses')
