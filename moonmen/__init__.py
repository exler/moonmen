import os

from flask import Flask, redirect, url_for
from werkzeug.exceptions import NotFound, RequestEntityTooLarge

from moonmen.commands import init_db, init_project
from moonmen.db.base import close_db
from moonmen.handlers import page_not_found, request_entity_too_large
from moonmen.views import auth, dashboard, files, notes, timers


def create_app():
    app = Flask(__name__, static_url_path="/static")

    base_dir = os.path.dirname(__file__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        BASE_DIR=base_dir,
        UPLOAD_DIR=os.path.join(base_dir, "uploads"),
        DATABASE=os.path.join(base_dir, "moonmen.sqlite"),
        ALLOWED_EXTENSIONS=["txt", "pdf", "png", "jpg", "jpeg", "gif", "bmp", "zip", "7z", "json"],
        MAX_CONTENT_LENGTH=(10 * 1000 * 1000),  # 10 MB
        SESSION_COOKIE_SAMESITE="Strict",
    )
    app.teardown_appcontext(close_db)

    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)

    register_commands(app)
    register_blueprints(app)
    register_error_handlers(app)

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.index"))

    return app


def register_blueprints(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(files.bp)
    app.register_blueprint(timers.bp)


def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(init_project)


def register_error_handlers(app):
    app.register_error_handler(NotFound, page_not_found)
    app.register_error_handler(RequestEntityTooLarge, request_entity_too_large)
