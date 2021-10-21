from flask import Blueprint, render_template, session

from moonmen.db import query_db
from moonmen.decorators import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    instance_id = session["instance_id"]
    instance = query_db("SELECT description, repository FROM instances WHERE id = ?", [instance_id])[0]

    return render_template(
        "dashboard.html", instance_desc=instance["description"], instance_repo=instance["repository"]
    )
