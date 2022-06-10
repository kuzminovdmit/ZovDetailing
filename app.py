from flask import Flask, request, render_template, flash
from flask_mail import Mail, Message

from forms import AppointmentForm, ContactForm
from local_settings import populate_env_settings


app = populate_env_settings(Flask(__name__))
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
    app.run(debug=True)
