import asyncio
from os import getenv

from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, jsonify
from flask_mailing import Mail, Message

from forms import AppointmentForm, ContactForm


load_dotenv()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.secret_key = getenv('SECRET_KEY')
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS', False)
    app.config['MAIL_USE_SSL'] = getenv('MAIL_USE_SSL', True)
    app.config['RECIPIENT_MAIL'] = getenv('RECIPIENT_MAIL')
    mail.init_app(app)
    return app


app = create_app()


@app.get("/email")
async def simple_send(form):
    html = f'''ФИО: {form.get('name')}
    Телефон: {form.get('phone')}
    Email: {form.get('email')}
    '''
    subject = f'Запись на прием: {form.get("name")}'
    if form.get('message'):
        html += f'\nСообщение: {form.get("message")}'
        subject = f'Обратная связь от: {form.get("name")}'

    await mail.send_message(Message(
        subject=subject,
        recipients=[app.config['RECIPIENT_MAIL']],
        body=html, sender=app.config['MAIL_USERNAME']
    ))

    return jsonify(status_code=200, content={"message": "Сообщение отправлено."})


@app.route('/', methods=['POST', 'GET'])
async def index():
    form = AppointmentForm()
    success = False

    if request.method == 'POST':
        if form.validate_on_submit():
            await asyncio.gather(simple_send(form.data))
            success = True
        else:
            flash(form.errors)

    return render_template('index.html', form=form, success=success)


@app.route('/feedback', methods=['POST', 'GET'])
async def feedback():
    form = ContactForm()
    success = False

    if request.method == 'POST':
        if form.validate_on_submit():
            await asyncio.gather(simple_send(form.data))
            success = True
        else:
            flash(form.errors)

    return render_template('feedback.html', form=form, success=success)


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
