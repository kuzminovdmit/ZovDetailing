import settings

from flask import Flask, request, render_template
from flask_mailman import Mail, EmailMessage
from flask_wtf.csrf import CSRFProtect


mail = Mail()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.secret_key = settings.SECRET_KEY
    app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
    app.config['MAIL_PORT'] = settings.MAIL_PORT
    app.config['MAIL_SERVER'] = settings.MAIL_SERVER
    app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
    app.config['MAIL_DEFAULT_SENDER'] = settings.MAIL_DEFAULT_SENDER
    app.config['MAIL_DEFAULT_RECIPIENT'] = settings.MAIL_DEFAULT_RECIPIENT
    mail.init_app(app)
    csrf.init_app(app)
    return app


app = create_app()


def simple_send(form):
    subject = f'Запись на прием: {form.get("name")}'
    body = f'''ФИО: {form.get('name')}
Телефон: {form.get('phone')}
Email: {form.get('email')}'''

    if form.get('message'):
        subject = f'Обратная связь от: {form.get("name")}'
        body += f'\nСообщение: {form.get("message")}'

    EmailMessage(
        subject=subject, body=body, to=[app.config['MAIL_DEFAULT_RECIPIENT']]
    ).send()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        simple_send(request.form.to_dict())

    return render_template('index.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        simple_send(request.form.to_dict())

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
