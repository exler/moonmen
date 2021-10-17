import getpass
import os

import click
from flask import current_app
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from moonmen.db import get_db, query_db

cli = AppGroup("commands")

HEADER = """
  __ _  ___  ___  ___  __ _  ___ ___
 /  ' \\/ _ \\/ _ \\/ _ \\/  ' \\/ -_) _ \\
/_/_/_/\\___/\\___/_//_/_/_/_/\\__/_//_/
"""


@cli.command("init-db")
def init_db():
    db = get_db()

    with current_app.open_resource(
        os.path.join(current_app.config["BASE_DIR"], "db", "_schema.sql"), mode="r"
    ) as schema:
        db.executescript(schema.read())

    click.echo("Database initialized")


@cli.command("init-project")
@click.argument("project_name")
def init_project(project_name):
    click.echo(click.style(HEADER, fg="yellow"))
    click.echo(click.style(f"(!) Initializing project '{project_name}'", fg="yellow"))
    try:
        project_desc = input("description: ")
        project_repo = input("repository: ")
        project_password = getpass.getpass("password: ")
        project_password = generate_password_hash(project_password)

        query_db(
            "INSERT INTO instances (name, password, description, repository) VALUES (?, ?, ?, ?)",
            [project_name, project_password, project_desc, project_repo],
            commit=True,
        )

        click.echo(click.style("\n(!) Project details saved", fg="blue"))
    except KeyboardInterrupt:
        click.echo(click.style("\n(!) Project initialization canceled", fg="red"))
