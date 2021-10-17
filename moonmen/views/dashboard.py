from enum import Enum

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from moonmen.db import query_db
from moonmen.decorators import login_required

bp = Blueprint("dashboard", __name__)


@bp.context_processor
def utility_processor():
    return dict(get_status_name=TaskStatus.get_status_name)


class TaskStatus(Enum):
    TODO = 1, "To do"
    IN_PROGRESS = 2, "In progress"
    PAUSED = 3, "Paused"
    COMPLETED = 4, "Completed"

    @staticmethod
    def get_choices():
        return [member.value for member in list(TaskStatus)]

    @staticmethod
    def get_status_name(status):
        choices = TaskStatus.get_choices()
        for choice in choices:
            if choice[0] == status:
                return choice[1]
        return None


@bp.route("/", methods=["GET"])
@login_required
def index():
    instance_id = session["instance_id"]
    instance = query_db("SELECT description, repository FROM instances WHERE id = ?", [instance_id])[0]

    tasks = query_db("SELECT id, title, description, status FROM tasks WHERE instance_id = ?", [instance_id])

    return render_template(
        "dashboard.html",
        instance_desc=instance["description"],
        instance_repo=instance["repository"],
        tasks=tasks,
        statuses=TaskStatus.get_choices(),
    )


@bp.route("/tasks/add/", methods=["POST"])
@login_required
def add():
    task_title = request.form.get("title")
    task_description = request.form.get("description")
    task_status = request.form.get("status")

    query_db(
        "INSERT INTO tasks (title, description, status, instance_id) VALUES (?, ?, ?, ?)",
        [task_title, task_description, task_status, session["instance_id"]],
        commit=True,
    )
    flash("Task added successfully")

    return redirect(url_for("dashboard.index"))


@bp.route("/tasks/edit/<int:task_id>/", methods=["POST"])
@login_required
def edit(task_id):
    task_title = request.form.get("title")
    task_description = request.form.get("description")
    task_status = request.form.get("status")

    query_db(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ? AND instance_id = ?",
        [task_title, task_description, task_status, task_id, session["instance_id"]],
        commit=True,
    )
    flash("Task updated successfully")

    return redirect(url_for("dashboard.index"))


@bp.route("/tasks/delete/<int:task_id>/", methods=["GET"])
@login_required
def delete(task_id):
    query_db("DELETE FROM tasks WHERE id = ? AND instance_id = ?", [task_id, session["instance_id"]], commit=True)
    flash("Task deleted successfully")

    return redirect(url_for("dashboard.index"))
