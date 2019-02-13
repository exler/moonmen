#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import packages
import os
import json
import argparse

# Import from project
from moonmen.web import app

# Color variables
BLUE, RED, YELLOW, END = "\033[94m", "\033[91m", "\033[93m", "\033[0m"


def new_project(project_name, password):
    with open("storage/{}.json".format(project_name), "w") as json_file:
        project_data = {
            "password": password,
            "details": {
                "description": None,
                "url": None
            }
        }

        json.dump(project_data, json_file, indent=4, sort_keys=True)


def load_project(project_name):
    with open("storage/{}.json".format(project_name)) as json_file:
        project_data = json.load(json_file)
        os.environ["PROJECT_NAME"] = project_name

        if project_data["password"] is not None:
            os.environ["PROJECT_PASSWORD"] = project_data["password"]
        else:
            os.environ["PROJECT_PASSWORD"] = ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("project",
                        help="Name of the project to run the server for.")
    parser.add_argument("-p", "--password",
                        help="Secure new project's web dashboard with password")
    args = parser.parse_args()

    if os.path.isfile("storage/{}.json".format(args.project)):
        load_project(args.project)

        app.secret_key = os.urandom(24)
        app.run(debug=True)
    else:
        new_project(args.project, args.password)
        print("{}(!) New project created!{}".format(BLUE, END))
