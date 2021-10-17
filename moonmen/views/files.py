import os
import uuid

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from moonmen.db import query_db
from moonmen.decorators import login_required

bp = Blueprint("files", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


def get_upload_path(filename):
    return os.path.join(current_app.config["UPLOAD_DIR"], filename)


@bp.route("/files/", methods=["GET"])
@login_required
def index():
    files = query_db("SELECT id, name FROM files WHERE instance_id = ?", [session["instance_id"]])

    return render_template("files.html", files=files)


@bp.route("/files/upload/", methods=["POST"])
@login_required
def upload():
    file = request.files["file"]

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = uuid.uuid4().hex

        query_db(
            "INSERT INTO files (name, path, instance_id) VALUES (?, ?, ?)",
            [filename, path, session["instance_id"]],
            commit=True,
        )

        file.save(get_upload_path(path))

        flash("File uploaded successfully")
    else:
        flash("Wrong filetype!")

    return redirect(url_for("files.index"))


@bp.route("/files/download/<int:file_id>/")
@login_required
def download(file_id):
    f = query_db("SELECT name, path FROM files WHERE id = ? AND instance_id = ?", [file_id, session["instance_id"]])[0]
    return send_file(get_upload_path(f["path"]), download_name=f["name"], as_attachment=True)


@bp.route("/files/delete/<int:file_id>/")
@login_required
def delete(file_id):
    file = query_db("SELECT path FROM files WHERE id = ? AND instance_id = ?", [file_id, session["instance_id"]])[0]
    os.remove(get_upload_path(file["path"]))
    query_db("DELETE FROM files WHERE id = ? AND instance_id = ?", [file_id, session["instance_id"]], commit=True)
    flash("File deleted successfully")

    return redirect(url_for("files.index"))
