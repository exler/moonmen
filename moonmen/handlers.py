from flask import flash, redirect


def page_not_found(e):
    flash("Not found! Please check the URL and try again.")
    return redirect("/"), 404


def request_entity_too_large(e):
    flash("File is too big!")
    return redirect("/files"), 413
