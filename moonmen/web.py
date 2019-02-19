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
        session["events"] = config["events"]

        return render_template("dashboard.html",
                               projectname=os.environ["PROJECT_NAME"],
                               projectdesc=config["details"]["description"],
                               projectrepo=config["details"]["repository"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/tasks")
def tasks():
    if session.get("logged_in") or not config["password"]:
        session["tasks"] = config["tasks"]

        return render_template("tasks.html",
                               projectname=os.environ["PROJECT_NAME"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
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
@app.route("/api/calendar_add")
def calendar_add():
    if session.get("logged_in") or not config["password"]:
        config["events"].append({"id": len(config["events"]), "name": "New Event", "summary": "Waiting to be edited...", "end_date": None})

        with open("storage/{}.json".format(os.environ["PROJECT_NAME"]), "w") as json_file:
            json.dump(config, json_file, indent=4)

    return redirect("/")


@app.route("/api/calendar_edit")
def calendar_edit():

    return redirect("/")


@app.route("/api/calendar_delete")
def calendar_delete():
    if session.get("logged_in") or not config["password"]:
        for idx, val in enumerate(config["events"]):
            if val["id"] == int(request.args.get("id")):
                del config["events"][idx]

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
