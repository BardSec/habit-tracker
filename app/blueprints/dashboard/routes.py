from flask import render_template
from flask_login import login_required, current_user

from app.blueprints.dashboard import bp
from app.services.dashboard_service import get_dashboard_data


@bp.route("/")
@login_required
def index():
    data = get_dashboard_data(current_user.id)
    return render_template("dashboard/index.html", **data)
