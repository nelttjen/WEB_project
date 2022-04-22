import sqlalchemy.exc
from flask import request, render_template, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from Site import app, login_manager, db
from Site.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['post', 'get'])
def login():
    _login = ""
    if current_user.get_id():
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_login = request.form.get('login')
        password = request.form.get('pass')
        user_db = User.query.filter_by(login=user_login).first()
        if user_db and check_password_hash(user_db.password, password):
            login_user(user_db)
            return redirect(url_for('profile'))
        else:
            flash("Логин или пароль неверны")
            _login = user_login
    return render_template("login.html", title='Авторизация', css=url_for('static', filename='css/login.css'),
                           login=_login)


@app.route('/register', methods=['post', 'get'])
def register():
    if current_user.get_id():
        return redirect(url_for('index'))

    ref = request.args.get('ref')
    fref = f'''value={ref} readonly''' if ref else ""
    if request.method == "POST":
        user_login = request.form.get("login")
        user_password = generate_password_hash(request.form.get("pass1"))
        day, month, year = [int(request.form.get(key)) for key in ["Day", "Month", "Year"]]
        if (day == 30 or day == 31) and month == 2:
            day = 29
        if day == 29 and month == 2 and year % 4:
            day = 28
        refer = request.form.get("referal") if request.form.get("referal") else -1
        try:
            refer_id = int(refer)
        except ValueError:
            refer_id = None
        refer_db = User.query.filter_by(id=refer_id).first()
        if not refer_db and refer_id != -1:
            flash("Неверный реферальный код")
        elif not all([1 <= day <= 31, 1 <= month <= 12, 1898 <= year <= 2022]):
            flash('Неправильная дата рождения')
        else:
            try:
                new_user = User(login=user_login,
                                password=user_password,
                                parent=refer,
                                day=day,
                                month=month,
                                year=year)
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация успешна')
                return redirect(url_for("login"))
            except sqlalchemy.exc.IntegrityError as e:
                flash("Логин уже занят!")

    return render_template('register.html', title='Регистрация', css=url_for('static', filename='css/register.css'),
                           info="", referal=fref)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.get_id():
        logout_user()
    return redirect(url_for("login"))


@app.route('/recovery', methods=["GET", 'POST'])
def recovery():
    if current_user.get_id():
        return redirect('index')
    if request.method == 'POST':
        pass
    return render_template('recovery.html')