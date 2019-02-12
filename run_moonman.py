#!/usr/bin/env python

import os
import json
import argparse

BLUE, RED, YELLOW, END = "\033[94m", "\033[91m", "\033[93m", "\033[0m"


def new_project(project_name, password):
    with open("storage/{}.json".format(project_name), "w") as json_file:
        project_data = {
            "password": password
        }

        json.dump(project_data, json_file, indent=4, sort_keys=True)


def open_project(project_name):
    with open("storage/{}.json".format(project_name)) as json_file:
        project_data = json.load(json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pain-free project manager for small teams", add_help=False)
    parser.add_argument("project",
                        help="Name of the project to run the server for.")
    parser.add_argument("-p", "--password",
                        help="Secure new project's web dashboard with password")
    args = parser.parse_args()

    if os.path.isfile("storage/{}.json".format(args.project)):
        open_project(args.project)
    else:
        new_project(args.project, args.password)
        print("{}(!) New project created!{}".format(BLUE, END))
