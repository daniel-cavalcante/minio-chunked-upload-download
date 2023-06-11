import os
from typing import Any
from flask import Flask, render_template, request
from flask_cors import CORS
from minio import Minio

from werkzeug.utils import secure_filename

TEMPORARY_FILE_DIR = "/tmp/chunked-file-transfer"
TEMPORARY_BUCKET_NAME = "temporary-bucket"

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT") or "localhost:9000"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY") or "minioadmin"
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY") or "minioadmin"
MINIO_IS_SECURE = os.getenv("MINIO_IS_SECURE") or "False"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
storage = Minio(endpoint=MINIO_ENDPOINT,
                access_key=MINIO_ACCESS_KEY,
                secret_key=MINIO_SECRET_KEY,
                # accepts capitalization variants as in FALSE, False and false
                secure=MINIO_IS_SECURE.lower() in ['true'])


@app.route("/")
def index():
    return render_template("index.html")


def upload_to_storage(bucket_name: str,
                      object_name: str,
                      data: Any) -> bool:
    try:
        if not storage.bucket_exists(bucket_name):
            storage.make_bucket(bucket_name)
        result = storage.put_object(bucket_name,
                                    object_name,
                                    data.stream,
                                    length=-1,
                                    part_size=10*1024*1024)
    except Exception:
        raise
    else:
        return True if result else False


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["myFile"]
    assert file.filename is not None
    success = upload_to_storage(TEMPORARY_BUCKET_NAME,
                                secure_filename(file.filename),
                                data=file)

    return {"success": success}, 200


if __name__ == "__main__":
    app.run(debug=True)
