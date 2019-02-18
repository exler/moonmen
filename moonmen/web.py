# Import packages
import os
import hashlib
from flask import Flask, flash, redirect, render_template, request, session
app = Flask(__name__, static_url_path="/static")

# Routes
@app.route("/")
def dashboard():
    if session.get("logged_in") or not os.environ["PROJECT_PASSWORD"]:
        return render_template("dashboard.html",
                               projectname=os.environ["PROJECT_NAME"],
                               projectsummary=os.environ["PROJECT_SUMMARY"],
                               projectrepo=os.environ["PROJECT_REPO"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/tasks")
def tasks():
    if session.get("logged_in") or not os.environ["PROJECT_PASSWORD"]:
        return render_template("tasks.html",
                               projectname=os.environ["PROJECT_NAME"])
    else:
        return render_template("login.html", projectname=os.environ["PROJECT_NAME"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        hashed_password = hashlib.sha512(request.form["password"].encode("utf-8")).hexdigest()

        if hashed_password == os.environ["PROJECT_PASSWORD"]:
            session["logged_in"] = True
        else:
            flash("Wrong password!")

    return redirect("/")


@app.route("/logout")
def logout():
    if os.environ["PROJECT_PASSWORD"]:
        if session.get("logged_in"):
            session["logged_in"] = False

    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    flash("Not found! Please check the URL and try again.")
    return redirect("/")
