from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from moonmen.db import query_db
from moonmen.decorators import login_required

bp = Blueprint("auth", __name__)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        instance_name = request.form.get("instance")
        instance_password = request.form.get("password")

        instance = query_db("SELECT id, password FROM instances WHERE name = ?", [instance_name])

        if not instance:
            flash("No instance with given name")
        else:
            instance = instance[0]
            if check_password_hash(instance["password"], instance_password):
                session["instance_id"] = instance["id"]
                session["instance_name"] = instance_name
            else:
                flash("Wrong password")

        return redirect(url_for("index"))
    else:
        if "instance_id" in session:
            return redirect(url_for("index"))
        else:
            return render_template("login.html")


@bp.route("/logout/", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
