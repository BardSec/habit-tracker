from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(255), nullable=False, default="")
    role = db.Column(db.String(50), nullable=False, default="user")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    habits = db.relationship("Habit", back_populates="user", cascade="all, delete-orphan")

    @property
    def is_admin(self):
        return self.role == "admin"
