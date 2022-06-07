from email import message
from flask import Flask, request
from flask import render_template


def validate_name(name):
    if len(name.split(' ')) != 3:
        raise Exception('Неправильно заполнены ФИО!')
    return name


def validate_phone(phone):
    if len(phone) != 11:
        raise Exception('Неправильный формат номера телефона!')
    return phone


def validate_email(email):
    if '@' not in email:
        raise Exception('Неправильный формат Email!')
    return email


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    message = ''
    if request.method == 'POST':
        message = {
            'name': validate_name(request.form.get('name')),
            'phone': validate_phone(request.form.get('phone')),
            'email': validate_email(request.form.get('email')),
            'agree': request.form.get('agree')
        }
    return render_template('index.html', message=message)


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
    message = ''
    if request.method == 'POST':
        message = {
            'name': validate_name(request.form.get('name')),
            'phone': validate_phone(request.form.get('phone')),
            'email': validate_email(request.form.get('email')),
            'text': validate_email(request.form.get('text')),
            'agree': request.form.get('agree')
        }
    return render_template('feedback.html', message=message)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')