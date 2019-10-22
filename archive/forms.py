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

class RegisterForm(Form):
    name = StringField(
        'Username',
        validators = [DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email',
        validators = [DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators = [DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        validators = [DataRequired(), EqualTo('password', message='Passwords do not match.')]
    )

class LoginForm(Form):
    name = StringField(
        'Username'
    )
    password = PasswordField(
        'Password'
    )