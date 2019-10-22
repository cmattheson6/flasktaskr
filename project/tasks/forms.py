from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddTaskForm(Form):
    task_id = IntegerField()
    name = StringField('Task Name', validators=[DataRequired()])
    due_date = DateField(
        'Date Due (mm/dd/yyyy)',
        validators=[DataRequired()],
        format='%m/%d/%Y'
    )
    priority = SelectField(
        'Priority',
        validators=[DataRequired()],
        choices=[
            (str(i), str(i)) for i in range(1,11)
        ]
    )