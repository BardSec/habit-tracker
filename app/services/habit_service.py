from datetime import date, timedelta

from app.extensions import db
from app.models.habit import Habit
from app.models.check_in import CheckIn


def get_user_habits(user_id, active_only=True):
    query = Habit.query.filter_by(user_id=user_id)
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Habit.created_at).all()


def create_habit(user_id, name, description="", color="#0d6efd"):
    habit = Habit(user_id=user_id, name=name, description=description, color=color)
    db.session.add(habit)
    db.session.commit()
    return habit


def update_habit(habit, name, description="", color="#0d6efd"):
    habit.name = name
    habit.description = description
    habit.color = color
    db.session.commit()
    return habit


def delete_habit(habit):
    db.session.delete(habit)
    db.session.commit()


def toggle_check_in(habit_id, check_date=None):
    """Toggle a check-in for a habit on a given date. Returns (CheckIn, created)."""
    if check_date is None:
        check_date = date.today()

    existing = CheckIn.query.filter_by(habit_id=habit_id, date=check_date).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return None, False

    check_in = CheckIn(habit_id=habit_id, date=check_date)
    db.session.add(check_in)
    db.session.commit()
    return check_in, True


def get_check_ins_for_date(user_id, check_date=None):
    """Return set of habit_ids that have check-ins for the given date."""
    if check_date is None:
        check_date = date.today()

    results = (
        db.session.query(CheckIn.habit_id)
        .join(Habit)
        .filter(Habit.user_id == user_id, CheckIn.date == check_date)
        .all()
    )
    return {r.habit_id for r in results}


def get_current_streak(habit_id):
    """Count consecutive days ending today (or yesterday if not yet checked in today)."""
    today = date.today()
    check_in_dates = set(
        r.date
        for r in CheckIn.query.filter_by(habit_id=habit_id)
        .filter(CheckIn.date <= today)
        .order_by(CheckIn.date.desc())
        .limit(365)
        .all()
    )

    if not check_in_dates:
        return 0

    # Start from today, or yesterday if today isn't checked in
    current = today if today in check_in_dates else today - timedelta(days=1)
    if current not in check_in_dates:
        return 0

    streak = 0
    while current in check_in_dates:
        streak += 1
        current -= timedelta(days=1)

    return streak


def get_longest_streak(habit_id):
    """Find the longest consecutive day streak for a habit."""
    dates = sorted(
        r.date
        for r in CheckIn.query.filter_by(habit_id=habit_id)
        .order_by(CheckIn.date)
        .all()
    )

    if not dates:
        return 0

    longest = 1
    current = 1
    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest
