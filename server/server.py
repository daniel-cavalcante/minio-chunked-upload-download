from flask import Flask, render_template, request
from pathlib import Path

from werkzeug.utils import secure_filename

TEMPORARY_FILE_DIR="/tmp/chunked-file-transfer"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    assert file.filename is not None;
    file.save(Path(TEMPORARY_FILE_DIR) / secure_filename(file.filename))

    return { "success": True }, 200


if __name__ == "__main__":
    app.run(debug=True)
