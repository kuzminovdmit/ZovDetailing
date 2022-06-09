from flask import Flask, request
from flask import render_template

from validators import validate_email, validate_name, validate_phone


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = {
            'name': validate_name(request.form.get('name')),
            'phone': validate_phone(request.form.get('phone')),
            'email': validate_email(request.form.get('email')),
            'agree': request.form.get('agree')
        }
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()