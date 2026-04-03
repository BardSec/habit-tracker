from flask import redirect, url_for, flash, render_template, current_app
from flask_login import login_user, logout_user, login_required

from app.blueprints.auth import bp
from app.blueprints.auth.forms import DevLoginForm
from app.services.auth_service import get_or_create_user


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_app.config.get("sso_enabled"):
        # TODO: SSO redirect — for now fall through to dev login
        pass

    # Dev login fallback
    form = DevLoginForm()
    if form.validate_on_submit():
        user = get_or_create_user(form.email.data)
        login_user(user)
        flash("Signed in successfully.", "success")
        return redirect(url_for("habits.index"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for("auth.login"))
