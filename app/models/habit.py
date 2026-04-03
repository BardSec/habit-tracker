from app.extensions import db


class Habit(db.Model):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    color = db.Column(db.String(7), default="#0d6efd")  # Bootstrap primary
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", back_populates="habits")
    check_ins = db.relationship("CheckIn", back_populates="habit", cascade="all, delete-orphan")
