import functools

from flask import redirect, session, url_for


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if "instance_id" not in session:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view
