from flask import Flask, request, render_template, jsonify
from flask_mailman import Mail, EmailMessage
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import EmailField, StringField, TelField, TextAreaField
from wtforms.validators import Email, InputRequired, Regexp

import settings


mail = Mail()
csrf = CSRFProtect()


def create_application():
    application = Flask(__name__)
    application.secret_key = settings.SECRET_KEY
    application.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
    application.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
    application.config['MAIL_PORT'] = settings.MAIL_PORT
    application.config['MAIL_SERVER'] = settings.MAIL_SERVER
    application.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
    application.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
    application.config['MAIL_DEFAULT_SENDER'] = settings.MAIL_DEFAULT_SENDER
    application.config['MAIL_DEFAULT_RECIPIENT'] = settings.MAIL_DEFAULT_RECIPIENT
    mail.init_app(application)
    csrf.init_app(application)
    return application


app = create_application()


class MailForm(FlaskForm):
    name = StringField(validators=[
        InputRequired(message='Необходимо ввести своё имя'),
        Regexp(
            r"^(?=.{1,40}$)[а-яёА-ЯЁ]+(?:[-' ][а-яёА-ЯЁ]+)*$",
            message='Введите настоящее имя'
        )
    ])
    email = EmailField(validators=[
        InputRequired(message='Необходимо ввести электронную почту'),
        Email(message='Неправильный формат электронной почты (пример: k@s.to)')
    ])
    phone = TelField(validators=[
        InputRequired(message='Необходимо ввести номер телефона'),
        Regexp(
            r'^[\d]{11}$',
            message='Неправильный формат номера телефона (пример: 88005553535)'
        )
    ])
    message = TextAreaField()


@app.route('/mail', methods=['POST', 'GET'])
def mail():
    form = MailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.data.get('name')
            email = form.data.get('email')
            phone = form.data.get('phone')
            message = form.data.get("message")

            subject = f'Запись на прием: {name}'
            body = f'ФИО: {name}\nТелефон: {phone}\nEmail: {email}'

            if message:
                subject = f'Обратная связь от: {name}'
                body += f'\nСообщение: {message}'

            msg = EmailMessage(
                subject=subject, body=body,
                to=[app.config['MAIL_DEFAULT_RECIPIENT']]
            )

            msg.send()
            return jsonify(data=form.data)
        else:
            return jsonify(data=form.errors)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/promotion')
def promotion():
    return render_template('promotion.html')


@app.route('/prices')
def prices():
    return render_template('prices.html')


if __name__ == '__main__':
    app.run()
