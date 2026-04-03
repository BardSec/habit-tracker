from flask import Blueprint

bp = Blueprint("habits", __name__, url_prefix="/habits")

from app.blueprints.habits import routes  # noqa: E402, F401
