from flask import Blueprint


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/")
def home():
    return "<a href='/minio'>MinIO</a>"
