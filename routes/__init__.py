from .authentication import authentication_blueprint
from .comment import comment_blueprint
from .ingredient import ingredient_blueprint
from .language import language_blueprint
from .person import person_blueprint
from .picture import picture_blueprint
from .recipe import recipe_blueprint


def register_routes(app):
    app.register_blueprint(authentication_blueprint, url_prefix="/auth")
    app.register_blueprint(comment_blueprint, url_prefix="/comment")
    app.register_blueprint(ingredient_blueprint, url_prefix="/ingredient")
    app.register_blueprint(language_blueprint, url_prefix="/language")
    app.register_blueprint(person_blueprint, url_prefix="/person")
    app.register_blueprint(picture_blueprint, url_prefix="/picture")
    app.register_blueprint(recipe_blueprint, url_prefix="/recipe")
