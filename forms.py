from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, StringField, TelField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class AppointmentForm(FlaskForm):
    name = StringField(validators=[DataRequired(message='Вы не ввели ФИО.')])
    email = EmailField(validators=[DataRequired(message='Вы не ввели email.')])
    phone = TelField(validators=[DataRequired(message='Вы не ввели телефон.')])
    agree = BooleanField()
    submit = SubmitField()


class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired(message='Вы не ввели ФИО.')])
    email = EmailField(validators=[DataRequired(message='Вы не ввели email.')])
    phone = TelField(validators=[DataRequired(message='Вы не ввели телефон.')])
    message = TextAreaField(validators=[InputRequired(message='Вы не написали сообщение.')])
    agree = BooleanField()
    submit = SubmitField()
