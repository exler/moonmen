from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from moonmen.db import query_db
from moonmen.decorators import login_required

bp = Blueprint("notes", __name__)


@bp.route("/notes/", methods=["GET"])
@login_required
def index():
    notes = query_db("SELECT id, title, content FROM notes WHERE instance_id = ?", [session["instance_id"]])

    return render_template(
        "notes.html",
        notes=notes,
    )


@bp.route("/notes/add/", methods=["POST"])
@login_required
def add():
    note_title = request.form.get("title")
    note_content = request.form.get("content")

    query_db(
        "INSERT INTO notes (title, content, instance_id) VALUES (?, ?, ?)",
        [note_title, note_content, session["instance_id"]],
        commit=True,
    )
    flash("Note added successfully")

    return redirect(url_for("notes.index"))


@bp.route("/notes/edit/<int:note_id>/", methods=["POST"])
@login_required
def edit(note_id):
    note_title = request.form.get("title")
    note_content = request.form.get("content")

    query_db(
        "UPDATE notes SET title = ?, content = ? WHERE id = ? AND instance_id = ?",
        [note_title, note_content, note_id, session["instance_id"]],
        commit=True,
    )
    flash("Note updated successfully")

    return redirect(url_for("notes.index"))


@bp.route("/notes/delete/<int:note_id>/", methods=["GET"])
@login_required
def delete(note_id):
    query_db("DELETE FROM notes WHERE id = ? AND instance_id = ?", [note_id, session["instance_id"]], commit=True)
    flash("Note deleted successfully")

    return redirect(url_for("notes.index"))
