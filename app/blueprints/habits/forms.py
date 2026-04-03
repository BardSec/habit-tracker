from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class HabitForm(FlaskForm):
    name = StringField("Habit Name", validators=[DataRequired(), Length(max=255)])
    description = TextAreaField("Description (optional)", validators=[Length(max=500)])
    color = StringField("Color", default="#0d6efd")
    submit = SubmitField("Save Habit")
