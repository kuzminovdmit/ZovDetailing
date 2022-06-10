from flask import Flask, request, render_template, flash
from flask_mail import Mail, Message
from os import getenv

from forms import AppointmentForm, ContactForm


app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS', False)
app.config['MAIL_USE_SSL'] = getenv('MAIL_USE_SSL', True)

mail = Mail()
mail.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    form = AppointmentForm()
    success = False
    
    if request.method == 'POST':
        if form.validate_on_submit():
            mail.send(Message(
                subject=f'Запись на прием пользователя {form.name.data}',
                recipients=[app.config['RECIPIENT_MAIL']],
                body=f'''
                ФИО: {form.name.data}
                Телефон: {form.phone.data}
                Email: {form.email.data}
                ''',
                sender=form.email.data
            ))
            success = True
        else:
            flash(form.errors)
        
    return render_template('index.html', form=form, success=success)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/promotion')
def promotion():
    return render_template('promotion.html')


@app.route('/prices')
def prices():
    return render_template('prices.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    form = ContactForm()
    success = False
    
    if request.method == 'POST':
        if form.validate_on_submit():
            mail.send(Message(
                subject=f'Сообщение от пользователя {form.name.data}',
                recipients=[app.config['RECIPIENT_MAIL']],
                body=f'''
                ФИО: {form.name.data}
                Телефон: {form.phone.data}
                Email: {form.email.data}
                Сообщение:
                {form.message.data}
                ''',
                sender=form.email.data
            ))
            success = True
        else:
            flash(form.errors)
        
    return render_template('feedback.html', form=form, success=success)


if __name__ == '__main__':
    app.run()
