from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

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
            return render_template("auth/login.html")


@bp.route("/logout/", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/change-password/", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password", "")
        new_password = request.form.get("new_password", "")
        new_password_confirmation = request.form.get("new_password_confirmation", "")

        instance = query_db("SELECT password FROM instances WHERE id = ?", [session["instance_id"]])[0]

        if not check_password_hash(instance["password"], old_password):
            flash("Old password is not valid")
        elif new_password != new_password_confirmation:
            flash("Password confirmation does not match the new password")
        elif new_password == old_password:
            flash("New password cannot be the same as old password")
        else:
            query_db("UPDATE instances SET password = ?", [generate_password_hash(new_password)], commit=True)
            flash("Password changed successfully")
            return redirect(url_for("index"))

    return render_template("auth/change_password.html")
