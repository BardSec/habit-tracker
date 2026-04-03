from datetime import date

from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app.blueprints.habits import bp
from app.blueprints.habits.forms import HabitForm
from app.models.habit import Habit
from app.services import habit_service


@bp.route("/")
@login_required
def index():
    habits = habit_service.get_user_habits(current_user.id)
    today_check_ins = habit_service.get_check_ins_for_date(current_user.id)
    return render_template(
        "habits/index.html",
        habits=habits,
        today_check_ins=today_check_ins,
        today=date.today(),
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = HabitForm()
    if form.validate_on_submit():
        habit_service.create_habit(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            color=form.color.data,
        )
        flash("Habit created!", "success")
        return redirect(url_for("habits.index"))
    return render_template("habits/create.html", form=form)


@bp.route("/<int:habit_id>/edit", methods=["GET", "POST"])
@login_required
def edit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    form = HabitForm(obj=habit)
    if form.validate_on_submit():
        habit_service.update_habit(
            habit, name=form.name.data, description=form.description.data, color=form.color.data
        )
        flash("Habit updated.", "success")
        return redirect(url_for("habits.index"))
    return render_template("habits/edit.html", form=form, habit=habit)


@bp.route("/<int:habit_id>/delete", methods=["POST"])
@login_required
def delete(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    habit_service.delete_habit(habit)
    flash("Habit deleted.", "info")
    return redirect(url_for("habits.index"))


@bp.route("/<int:habit_id>/toggle", methods=["POST"])
@login_required
def toggle(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    _, created = habit_service.toggle_check_in(habit_id)
    if created:
        flash(f"'{habit.name}' checked off for today!", "success")
    else:
        flash(f"'{habit.name}' unchecked for today.", "info")
    return redirect(url_for("habits.index"))
