from datetime import datetime
from flask import Flask

from source.routes.home import home_blueprint
from source.routes.minio import minio_blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from source.database import db

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:1234@localhost:5432/postgres"
    db.init_app(app)

    app.register_blueprint(home_blueprint, url_prefix="/")
    app.register_blueprint(minio_blueprint, url_prefix="/minio")

    return app


if __name__ == "__main__":
    app = create_app()
    print(f"[{datetime.now()}] STARTING SERVER...")
    app.run(host="0.0.0.0", port=5000, debug=True)
