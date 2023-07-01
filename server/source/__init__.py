from flask import Flask

from .routes import blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(blueprint)

    return app
