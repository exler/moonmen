#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import packages
import os
import json
import argparse
import getpass
import hashlib
from gevent.pywsgi import WSGIServer

# Console interface
BLUE, RED, YELLOW, END = "\033[94m", "\033[91m", "\033[93m", "\033[0m"
HEADER = """
  __ _  ___  ___  ___  __ _  ___ ___
 /  ' \\/ _ \\/ _ \\/ _ \\/  ' \\/ -_) _ \\
/_/_/_/\\___/\\___/_//_/_/_/_/\\__/_//_/
         """


def create_project(project_name, project_password, project_desc, project_repo):
    os.mkdir("storage/{}".format(project_name))

    with open("storage/{}.json".format(project_name), "w") as json_file:
        project_data = {
            "password": project_password,
            "details": {
                "description": project_desc,
                "repository": project_repo
            },
            "tasks": [],
            "file_extensions": ["txt", "pdf", "png", "jpg", "jpeg", "gif", "zip"],
            "files": [],
            "notes": []
        }

        json.dump(project_data, json_file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("project",
                        help="Name of the project to run the server for.")
    parser.add_argument("-p", "--port", default=8080, type=int,
                        help="Available port to run the web server on.")
    parser.add_argument("--debug", action="store_true",
                        help="Use Flask's built-in development server instead of Gevent.")
    args = parser.parse_args()

    if os.path.isfile("storage/{}.json".format(args.project)):
        print(BLUE + HEADER + END)

        os.environ["PROJECT_NAME"] = args.project
        os.environ["BASEDIR"] = os.path.abspath(os.path.dirname(__file__))

        from moonmen.web import app
        app.secret_key = os.urandom(24)

        if args.debug:
            app.run(debug=True, port=args.port)
        else:
            try:
                print("Listening for requests on port {}...\n\n".format(args.port))
                http_server = WSGIServer(('', args.port), app)
                http_server.serve_forever()
            except KeyboardInterrupt:
                print("\n\n{}(!) Closing webserver...{}".format(RED, END))
    else:
        print(YELLOW + HEADER + END)
        print("{}(!) Initialize project '{}'...\n{}".format(YELLOW, args.project, END))
        try:
            project_desc = input("description: ")
            project_repo = input("repository: ")
            project_password = getpass.getpass("password: ")

            if project_password is not "":
                project_password = hashlib.sha512(project_password.encode("utf-8")).hexdigest()

            create_project(args.project, project_password, project_desc, project_repo)

            print("\n{}(!) Project details saved.{}".format(BLUE, END))
        except KeyboardInterrupt:
            print("\n\n{}(!) Project initialization canceled.{}".format(RED, END))
