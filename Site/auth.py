from flask import request, render_template, url_for
from werkzeug.security import generate_password_hash

from Site import app


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
    ref = request.args.get('ref')
    fref = f'''value={ref} disabled''' if ref else ""
    if request.method == "POST":
        return 'register'

    return render_template('register.html', title='Регистрация', css=url_for('static', filename='css/register.css'),
                           info="", referal=fref)