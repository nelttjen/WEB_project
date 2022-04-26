import datetime
import random

import sqlalchemy.exc
from flask import request, render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from Site import app, login_manager, db
from Site.models import User, ConfirmCode


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def normalize_date(day, month, year):
    if (day == 30 or day == 31) and month == 2:
        day = 29
    if day == 29 and month == 2 and year % 4:
        day = 28
    return day, month, year


def delete_if_not_valid(model: ConfirmCode, _login):
    _d, _m, _y, _h, _min, _s = map(int, model.creation.split('.'))
    creation = datetime.datetime(_y, _m, _d, _h, _min, _s)
    now = datetime.datetime.now()
    if now > creation + datetime.timedelta(minutes=int(model.valid_mins)):
        ConfirmCode.query.filter_by(login_for=_login).delete()
        db.session.commit()
        return True
    return False


def generate_code(login_for):
    code = str(random.randint(1, 999999)).zfill(6)
    _new = ConfirmCode(
        login_for=login_for,
        creation=datetime.datetime.now().strftime('%d.%m.%Y.%H.%M.%S'),
        code=code
    )
    db.session.add(_new)
    db.session.commit()


@app.route('/login', methods=['post', 'get'])
def login():
    _login = ""
    if current_user.get_id():
        return redirect(url_for('index'))
    _class = 'info' if not request.args.get('recovery') and not request.args.get('logout') else 'info-green'
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
        if _class == 'info-green':
            return redirect(url_for('login'))
    return render_template("login.html", title='Авторизация', css=url_for('static', filename='css/login.css'),
                           login=_login, user=None, info_class=_class)


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
        day, month, year = normalize_date(day, month, year)
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
            except sqlalchemy.exc.IntegrityError:
                flash("Логин уже занят!")

    return render_template('register.html', title='Регистрация', css=url_for('static', filename='css/register.css'),
                           info="", referal=fref, user=None)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.get_id():
        logout_user()
        flash('Вы вышли из аккаунта')
        return redirect(url_for('login', logout=1))
    return redirect(url_for("login"))


@app.route('/recovery', methods=["GET", 'POST'])
def recovery():
    if current_user.get_id():
        return redirect('index')
    args_login = request.args.get('login')
    _login, _code = [None] * 2
    if args_login:
        usr = User.query.filter_by(login=args_login).first()
        if usr:
            _login = args_login
            db_code = ConfirmCode.query.filter_by(login_for=_login).first()
            if not db_code:
                flash('Код устарел, получите новый код')
                return redirect(url_for('recovery'))
            else:
                if delete_if_not_valid(db_code, _login):
                    flash('Код устарел, получите новый код')
                    return redirect(url_for('recovery'))
            _code = db_code.code
        else:
            flash('Неизвестный логин')
            return redirect(url_for('recovery'))
    if request.method == 'POST':
        if not args_login:
            _login = request.form.get('login')
            if not _login or not User.query.filter_by(login=_login).first():
                flash('Неизвестный логин')
                return redirect(url_for('recovery'))
            else:
                _test = ConfirmCode.query.filter_by(login_for=_login).first()
                if _test:
                    if delete_if_not_valid(_test, _login):
                        _test = False
                if not _test:
                    generate_code(_login)
                return redirect(url_for('recovery', login=_login))
        else:
            pass1, pass2 = request.form.get('pass1'), request.form.get('pass2')
            code = ConfirmCode.query.filter_by(login_for=_login).first()
            form_code = request.form.get('confirm')
            usr = User.query.filter_by(login=_login).first()
            if delete_if_not_valid(code, _login):
                flash('Код устарел, получите новый код')
            elif code.code != form_code:
                flash('Код неверен!')
            elif check_password_hash(usr.password, pass1):
                flash('Пароль не может совпадать с текущим')
            else:
                usr.password = generate_password_hash(pass1)
                ConfirmCode.query.filter_by(login_for=_login).delete()
                db.session.commit()
                flash('Пароль успешно изменен')
                return redirect(url_for('login', recovery=1))
    return render_template('recovery.html', user=None, css=url_for('static', filename='css/recovery.css'),
                           login=_login, code=_code)
