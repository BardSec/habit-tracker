from datetime import date, timedelta
from collections import defaultdict

from sqlalchemy import func

from app.extensions import db
from app.models.habit import Habit
from app.models.check_in import CheckIn
from app.services.habit_service import get_current_streak, get_longest_streak


def get_dashboard_data(user_id):
    """Assemble all dashboard stats for a user."""
    habits = Habit.query.filter_by(user_id=user_id, is_active=True).all()

    habit_stats = []
    for habit in habits:
        current = get_current_streak(habit.id)
        longest = get_longest_streak(habit.id)
        total = CheckIn.query.filter_by(habit_id=habit.id).count()
        habit_stats.append({
            "habit": habit,
            "current_streak": current,
            "longest_streak": longest,
            "total_check_ins": total,
        })

    return {
        "habit_stats": habit_stats,
        "weekly_data": _get_weekly_completion(user_id, habits),
        "monthly_data": _get_monthly_completion(user_id, habits),
        "overall_rate": _get_overall_completion_rate(user_id, habits),
    }


def _get_weekly_completion(user_id, habits):
    """Completion counts for the last 7 days."""
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    habit_ids = [h.id for h in habits]

    if not habit_ids:
        return {"labels": [d.strftime("%a") for d in days], "data": [0] * 7}

    results = (
        db.session.query(CheckIn.date, func.count(CheckIn.id))
        .filter(CheckIn.habit_id.in_(habit_ids), CheckIn.date.in_(days))
        .group_by(CheckIn.date)
        .all()
    )
    counts = dict(results)

    return {
        "labels": [d.strftime("%a") for d in days],
        "data": [counts.get(d, 0) for d in days],
        "max": len(habits),
    }


def _get_monthly_completion(user_id, habits):
    """Weekly completion rates for the last 4 weeks."""
    today = date.today()
    habit_ids = [h.id for h in habits]
    weeks = []

    for w in range(3, -1, -1):
        week_end = today - timedelta(days=7 * w)
        week_start = week_end - timedelta(days=6)
        weeks.append((week_start, week_end))

    if not habit_ids:
        return {"labels": [f"Week {i+1}" for i in range(4)], "data": [0] * 4}

    data = []
    labels = []
    for week_start, week_end in weeks:
        total_possible = len(habits) * 7
        actual = (
            CheckIn.query
            .filter(
                CheckIn.habit_id.in_(habit_ids),
                CheckIn.date >= week_start,
                CheckIn.date <= week_end,
            )
            .count()
        )
        rate = round((actual / total_possible) * 100) if total_possible > 0 else 0
        data.append(rate)
        labels.append(f"{week_start.strftime('%m/%d')}")

    return {"labels": labels, "data": data}


def _get_overall_completion_rate(user_id, habits):
    """Overall completion rate for the last 30 days."""
    if not habits:
        return 0

    today = date.today()
    start = today - timedelta(days=29)
    habit_ids = [h.id for h in habits]

    total_possible = len(habits) * 30
    actual = (
        CheckIn.query
        .filter(
            CheckIn.habit_id.in_(habit_ids),
            CheckIn.date >= start,
            CheckIn.date <= today,
        )
        .count()
    )
    return round((actual / total_possible) * 100) if total_possible > 0 else 0
