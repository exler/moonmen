# Import packages
import os
import json
import hashlib
from flask import Flask, flash, redirect, render_template, request, session
app = Flask(__name__, static_url_path="/static")

# Configuration file
with open("storage/{}.json".format(os.environ["PROJECT_NAME"])) as json_file:
    config = json.load(json_file)

# Routes
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


@app.route("/resources")
def tasks():
    if session.get("logged_in") or not config["password"]:
        return render_template("resources.html",
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

# API routes
@app.route("/api/tasks_add", methods=["POST"])
def tasks_add():
    if session.get("logged_in") or not config["password"]:
        if len(request.form["name-input"]) > 30 or len(request.form["description-input"]) > 50:
            flash("Input too long!")
        else:
            config["tasks"].append({"id": len(config["tasks"]),
                                    "name": request.form["name-input"],
                                    "description": request.form["description-input"],
                                    "status": request.form["status-select"]})

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)

    return redirect("/")


@app.route("/api/tasks_edit", methods=["POST"])
def tasks_edit():
    if session.get("logged_in") or not config["password"]:
        if len(request.form["name-input"]) > 30 or len(request.form["description-input"]) > 50:
            flash("Input too long!")
        else:
            for idx, val in enumerate(config["tasks"]):
                if val["id"] == int(request.args.get("id")):
                    config["tasks"][idx]["name"] = request.form["name-input"]
                    config["tasks"][idx]["description"] = request.form["description-input"]
                    config["tasks"][idx]["status"] = request.form["status-select"]

            with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
                json.dump(config, json_file, indent=4)

    return redirect("/")


@app.route("/api/tasks_delete")
def tasks_delete():
    if session.get("logged_in") or not config["password"]:
        for idx, val in enumerate(config["tasks"]):
            if val["id"] == int(request.args.get("id")):
                del config["tasks"][idx]

        with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
            json.dump(config, json_file, indent=4)

    return redirect("/")


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    flash("Not found! Please check the URL and try again.")
    return redirect("/")


@app.errorhandler(405)
def method_not_allowed(e):
    flash("Method not allowed! Please do not type URLs manually.")
    return redirect("/")
