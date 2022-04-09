from flask import Flask, render_template, url_for, request
from werkzeug.security import generate_password_hash
from App.Config import Config
from App.settings import *

app = Flask(__name__)
config = Config(app)


@app.route('/')
def index():
    return render_template("base.html", css=url_for('static', filename='css/index.css'))


@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        print(email, "\n", generate_password_hash(password))
        return "login"
    return render_template("login.html", title='Авторизация', css=url_for('static', filename='css/login.css'))


@app.route('/register', methods=['post', 'get'])
def register():
    ref = request.args.get('ref') if request.args.get('ref') else -1

    return render_template('register.html', title='Регистрация', css=url_for('static', filename='css/register.css'))


if __name__ == '__main__':
    config.set('SECRET_KEY', SECRET_KEY)
    print(config.get('SECRET_KEY'))
    app.run(port=8080)
