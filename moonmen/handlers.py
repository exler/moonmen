from flask import flash, redirect, url_for


def page_not_found(e):
    flash("Not found! Please check the URL and try again.")
    return redirect(url_for("dashboard.index")), 404


def request_entity_too_large(e):
    flash("File is too big!")
    return redirect(url_for("files.index")), 413
