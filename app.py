from flask import Flask

from source.routes import minio_blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(minio_blueprint, url_prefix="/minio")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
