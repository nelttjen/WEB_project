from flask import request, render_template, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from Site import app, login_manager, db
from Site.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        user_login = request.form.get('login')
        password = request.form.get('pass')
        user_db = User.query.filter_by(login=user_login).first()
        if user_db and check_password_hash(user_db.password, password):
            login_user(user_db)
        else:
            flash("Логин или пароль неверны")
    return render_template("login.html", title='Авторизация', css=url_for('static', filename='css/login.css'))


@app.route('/register', methods=['post', 'get'])
def register():
    ref = request.args.get('ref')
    fref = f'''value={ref} disabled''' if ref else ""
    if request.method == "POST":
        user_login = request.form.get("login")
        user_password = generate_password_hash(request.form.get("pass1"))
        day, month, year = [int(request.form.get(key)) for key in ["Day", "Month", "Year"]]
        if day == 29 and month == 2 and year % 4:
            day = 28
        refer = request.form.get("refer") if request.form.get("refer") else -1
        try:
            new_user = User(login=user_login, password=user_password,
                            parent=refer, day=day, month=month, year=year)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e.__class__)
        return 'register'

    return render_template('register.html', title='Регистрация', css=url_for('static', filename='css/register.css'),
                           info="", referal=fref)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))