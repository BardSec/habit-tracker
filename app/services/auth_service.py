from flask import current_app

from app.extensions import db
from app.models.user import User


def get_or_create_user(email, display_name=""):
    """Find existing user by email or create a new one.
    First user matching ADMIN_EMAILS gets admin role."""
    user = User.query.filter_by(email=email).first()
    if user:
        return user

    role = "user"
    if email in current_app.config["ADMIN_EMAILS"]:
        role = "admin"

    user = User(email=email, display_name=display_name or email, role=role)
    db.session.add(user)
    db.session.commit()
    return user
