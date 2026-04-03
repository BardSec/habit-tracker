from datetime import date

from app.models.user import User
from app.models.habit import Habit
from app.models.check_in import CheckIn
from app.extensions import db


def test_create_user(app):
    with app.app_context():
        user = User(email="test@example.com", display_name="Test User")
        db.session.add(user)
        db.session.flush()
        assert user.id is not None
        assert user.role == "user"
        assert not user.is_admin


def test_create_habit(app):
    with app.app_context():
        user = User(email="habits@example.com", display_name="Habit User")
        db.session.add(user)
        db.session.flush()

        habit = Habit(user_id=user.id, name="Exercise", description="30 min daily")
        db.session.add(habit)
        db.session.flush()
        assert habit.id is not None
        assert habit.is_active is True


def test_check_in(app):
    with app.app_context():
        user = User(email="checkin@example.com", display_name="Check User")
        db.session.add(user)
        db.session.flush()

        habit = Habit(user_id=user.id, name="Read")
        db.session.add(habit)
        db.session.flush()

        check_in = CheckIn(habit_id=habit.id, date=date.today())
        db.session.add(check_in)
        db.session.flush()
        assert check_in.id is not None
