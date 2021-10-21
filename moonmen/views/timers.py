from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from moonmen.db import query_db
from moonmen.decorators import login_required

bp = Blueprint("timers", __name__)


@bp.route("/timers/", methods=["GET"])
@login_required
def index():
    timers = query_db("SELECT id, name, dt FROM timers WHERE instance_id = ?", [session["instance_id"]])

    return render_template("timers.html", timers=timers)


@bp.route("/timers/add/", methods=["POST"])
@login_required
def add():
    timer_name = request.form.get("name")
    timer_dt = request.form.get("dt")

    query_db(
        "INSERT INTO timers (name, dt, instance_id) VALUES (?, ?, ?)",
        [timer_name, timer_dt, session["instance_id"]],
        commit=True,
    )
    flash("Timer added successfully")

    return redirect(url_for("timers.index"))


@bp.route("/timers/edit/<int:timer_id>/", methods=["POST"])
@login_required
def edit(timer_id):
    timer_name = request.form.get("name")
    timer_dt = request.form.get("dt")

    query_db(
        "UPDATE timers SET name = ?, dt = ? WHERE id = ? AND instance_id = ?",
        [timer_name, timer_dt, timer_id, session["instance_id"]],
        commit=True,
    )
    flash("Timer updated successfully")

    return redirect(url_for("timers.index"))


@bp.route("/timers/delete/<int:timer_id>/", methods=["GET"])
@login_required
def delete(timer_id):
    query_db("DELETE FROM timers WHERE id = ? AND instance_id = ?", [timer_id, session["instance_id"]], commit=True)
    flash("Timer deleted successfully")

    return redirect(url_for("timers.index"))
