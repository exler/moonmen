#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import packages
import os
import json
import argparse
import getpass

# Import from project
from moonmen.web import app

# Console interface
BLUE, RED, YELLOW, END = "\033[94m", "\033[91m", "\033[93m", "\033[0m"
HEADER = """
  __ _  ___  ___  ___  __ _  ___ ___
 /  ' \\/ _ \\/ _ \\/ _ \\/  ' \\/ -_) _ \\
/_/_/_/\\___/\\___/_//_/_/_/_/\\__/_//_/
         """


def new_project(project_name, project_password, project_summary, project_repo):
    with open("storage/{}.json".format(project_name), "w") as json_file:
        project_data = {
            "password": project_password,
            "details": {
                "summary": project_summary,
                "repository": project_repo
            }
        }

        json.dump(project_data, json_file, indent=4, sort_keys=True)


def load_project(project_name):
    with open("storage/{}.json".format(project_name)) as json_file:
        project_data = json.load(json_file)
        os.environ["PROJECT_NAME"] = project_name
        os.environ["PROJECT_SUMMARY"] = project_data["details"]["summary"]
        os.environ["PROJECT_REPO"] = project_data["details"]["repository"]

        if project_data["password"] is not None:
            os.environ["PROJECT_PASSWORD"] = project_data["password"]
        else:
            os.environ["PROJECT_PASSWORD"] = ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("project",
                        help="Name of the project to run the server for.")
    args = parser.parse_args()

    if os.path.isfile("storage/{}.json".format(args.project)):
        print(BLUE + HEADER + END)

        load_project(args.project)

        app.secret_key = os.urandom(24)
        app.run(debug=True)
    else:
        print(YELLOW + HEADER + END)
        print("{}(!) Initialize new project...\n{}".format(YELLOW, END))
        print("name: {}".format(args.project))
        try:
            project_summary = input("description: ")
            project_repo = input("repository: ")
            project_password = getpass.getpass("password: (none) ")

            new_project(args.project, project_password, project_summary, project_repo)

            print("\n\n{}(!) Project details saved.{}".format(BLUE, END))
        except KeyboardInterrupt:
            print("\n\n{}(!) Project initialization canceled.{}".format(RED, END))
