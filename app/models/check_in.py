from app.extensions import db


class CheckIn(db.Model):
    __tablename__ = "check_ins"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    habit = db.relationship("Habit", back_populates="check_ins")

    __table_args__ = (
        db.UniqueConstraint("habit_id", "date", name="uq_habit_date"),
    )
