# Imports
import os
import json
import hashlib
import random
import string
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path="/static")
app.config["UPLOAD_FOLDER"] = "{}/storage/{}".format(os.environ["BASEDIR"], os.environ["PROJECT_NAME"])
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

# Configuration file
with open("storage/{}.json".format(os.environ["PROJECT_NAME"])) as json_file:
    config = json.load(json_file)


############
#  Routes  #
############
@app.route("/")
def dashboard():
    if session.get("logged_in") or not config["password"]:
        session["tasks"] = config["tasks"]

        return render_template("dashboard.html",
                               projectname=os.environ["PROJECT_NAME"],
                               projectdesc=config["details"]["description"],
                               projectrepo=config["details"]["repository"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/notes")
def tasks():
    if session.get("logged_in") or not config["password"]:
        session["notes"] = config["notes"]

        return render_template("notes.html",
                               projectname=os.environ["PROJECT_NAME"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/files")
def files():
    if session.get("logged_in") or not config["password"]:
        session["files"] = config["files"]

        return render_template("files.html",
                               projectname=os.environ["PROJECT_NAME"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/login", methods=["POST"])
def login():
    hashed_password = hashlib.sha512(request.form["password"].encode("utf-8")).hexdigest()

    if hashed_password == config["password"]:
        session["logged_in"] = True
    else:
        flash("Wrong password!")

    return redirect("/")


@app.route("/logout")
def logout():
    if config["password"]:
        if session.get("logged_in"):
            session["logged_in"] = False

    return redirect("/")


################
#  API Routes  #
################
@app.route("/api/tasks_add", methods=["POST"])
def tasks_add():
    if session.get("logged_in") or not config["password"]:
        allowed_selections = ["Planned", "In Progress", "Paused", "Completed"]

        if len(request.form["name-input"]) > 30 or len(request.form["description-input"]) > 50:
            flash("Input too long!")
        elif len(request.form["name-input"]) == 0 or len(request.form["description-input"]) == 0:
            flash("Input too short!")
        elif request.form["status-select"] not in allowed_selections:
            flash("Not allowed status selected!")
        else:
            config["tasks"].append({"id": random_unique_id("tasks"),
                                    "title": request.form["name-input"],
                                    "description": request.form["description-input"],
                                    "status": request.form["status-select"]})

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)

    return redirect("/")


@app.route("/api/tasks_edit", methods=["POST"])
def tasks_edit():
    if session.get("logged_in") or not config["password"]:
        allowed_selections = ["Planned", "In Progress", "Paused", "Completed"]

        if len(request.form["name-input"]) > 30 or len(request.form["description-input"]) > 50:
            flash("Input too long!")
        elif len(request.form["name-input"]) == 0 or len(request.form["description-input"]) == 0:
            flash("Input too short!")
        elif request.form["status-select"] not in allowed_selections:
            flash("Not allowed status selected!")
        else:
            for idx, val in enumerate(config["tasks"]):
                if val["id"] == int(request.args.get("id")):
                    config["tasks"][idx]["title"] = request.form["name-input"]
                    config["tasks"][idx]["description"] = request.form["description-input"]
                    config["tasks"][idx]["status"] = request.form["status-select"]

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)

    return redirect("/")


@app.route("/api/tasks_delete/<task_id>")
def tasks_delete(task_id):
    if session.get("logged_in") or not config["password"]:
        for idx, val in enumerate(config["tasks"]):
            if val["id"] == int(task_id):
                del config["tasks"][idx]

        with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
            json.dump(config, json_file, indent=4)

    return redirect("/")


@app.route("/api/notes_add", methods=["POST"])
def notes_add():
    if session.get("logged_in") or not config["password"]:
        if len(request.form["title-input"]) > 30 or len(request.form["content-input"]) > 400:
            flash("Input too long!")
        elif len(request.form["title-input"]) == 0 or len(request.form["content-input"]) == 0:
            flash("Input too short!")
        else:
            config["notes"].append({"id": random_unique_id("notes"),
                                    "title": request.form["title-input"],
                                    "content": request.form["content-input"]})

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)

    return redirect("/notes")


@app.route("/api/notes_edit", methods=["POST"])
def notes_edit():
    if session.get("logged_in") or not config["password"]:
        if len(request.form["title-input"]) > 30 or len(request.form["content-input"]) > 400:
            flash("Input too long!")
        elif len(request.form["title-input"]) == 0 or len(request.form["content-input"]) == 0:
            flash("Input too short!")
        else:
            for idx, val in enumerate(config["notes"]):
                if val["id"] == int(request.args.get("id")):
                    config["notes"][idx]["title"] = request.form["title-input"]
                    config["notes"][idx]["content"] = request.form["content-input"]

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)

    return redirect("/notes")


@app.route("/api/notes_delete/<note_id>")
def notes_delete(note_id):
    if session.get("logged_in") or not config["password"]:
        for idx, val in enumerate(config["notes"]):
            if val["id"] == int(note_id):
                del config["notes"][idx]

        with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
            json.dump(config, json_file, indent=4)

    return redirect("/notes")


@app.route("/api/files_upload", methods=["POST"])
def files_upload():
    if session.get("logged_in") or not config["password"]:
        file = request.files["filesUpload"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            random_filename = "".join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "." + filename.rsplit('.', 1)[1].lower()

            config["files"].append({"id": random_unique_id("files"),
                                    "original_filename": filename,
                                    "random_filename": random_filename})

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], random_filename))

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)
        else:
            flash("Wrong filetype!")

    return redirect("/files")


@app.route("/api/files_download/<filename>")
def files_download(filename):
    if session.get("logged_in") or not config["password"]:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/api/files_delete/<file_id>")
def files_delete(file_id):
    if session.get("logged_in") or not config["password"]:
        for idx, val in enumerate(config["files"]):
            if val["id"] == int(file_id):
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], config["files"][idx]["random_filename"]))
                del config["files"][idx]

        with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
            json.dump(config, json_file, indent=4)

    return redirect("/files")


##################
# Error handlers #
##################
@app.errorhandler(404)
def page_not_found(e):
    flash("Not found! Please check the URL and try again.")
    return redirect("/")


@app.errorhandler(405)
def method_not_allowed(e):
    flash("Method not allowed! Please do not type URLs manually.")
    return redirect("/")


@app.errorhandler(413)
def request_entity_too_large(e):
    flash("File submitted exceeded maximum limit.")
    return redirect("/files")


#############
# Functions #
#############
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config["file_extensions"]


def random_unique_id(json_object_name):
    number = random.randint(1, 10000)

    for val in config[json_object_name]:
        if val["id"] == number:
            number = random.randint(1, 10000)

    return number
