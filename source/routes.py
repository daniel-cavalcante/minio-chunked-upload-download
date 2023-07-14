from flask import (
    Blueprint, Response, render_template, request, stream_with_context
)
from werkzeug.utils import secure_filename

from source.utils import get_file_chunks, get_filename, upload_to_storage
from source.storage import storage

minio_blueprint = Blueprint("minio",
                      __name__,
                      template_folder="templates",
                      static_folder="static")

@minio_blueprint.route("/")
def index():
    return render_template("index.html")


@minio_blueprint.route("/download")
def download():
    bucket_list = [bucket.name for bucket in storage.list_buckets()]
    return bucket_list


@minio_blueprint.route("/download/<string:bucket_name>")
def download_bucket(bucket_name):
    value = f"attachment; filename={get_filename(storage, bucket_name)}"
    return Response(
        stream_with_context(get_file_chunks(storage, bucket_name)),
        headers={"Content-Disposition": value},
    )


@minio_blueprint.route("/upload", methods=["POST"])
def upload():
    # todo: set some form of validation after uploading all files
    chunk = request.files["chunk"]
    original_file_id = request.form["originalFileId"]

    assert chunk.filename is not None
    name = secure_filename(chunk.filename)
    if name == "":
        # todo: return meaningful message to the client
        return {"success": False}, 500

    success = upload_to_storage(storage, original_file_id, name, data=chunk)
    return {"success": success}, 201
