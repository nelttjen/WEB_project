import datetime
import os.path

from flask import render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from datetime import date

from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from Site import app, db, launch
from Site.models import User, Apikey, BalanceRequest
from Site.settings import *
from Site.api import create_apikey


def get_user_nick():
    try:
        nick = User.query.get(current_user.get_id()).login
    except AttributeError:
        nick = None
    return nick


@app.route('/')
@app.route('/index')
def index():
    ref = request.args.get("ref")
    if ref:
        return redirect(url_for('register', ref=ref))
    return render_template("index.html",
                           css=url_for('static', filename='css/index.css'),
                           user=User.query.get(current_user.get_id()),
                           promo=None)


@app.route('/test')
def test():
    _delta = datetime.datetime.now() - launch
    h, m, s = str(_delta).split(', ')[1].split(':') if str(_delta).count(',') > 0 else str(_delta).split(':')
    stack = [int(_delta.days), int(h), int(m), int(float(s))]
    return f'{int(_delta.days)} days, {int(h)} hours, {int(m)} minutes, {int(float(s))} seconds'


@app.route('/profile', methods=["GET", 'POST'])
@login_required
def profile():
    profile_id = request.args.get('user_id')
    superuser = None
    if profile_id:
        superuser = User.query.get(current_user.get_id())
    cur_user = User.query.get(current_user.get_id())
    if request.method == "POST":
        cur_email = current_user.email
        new_email = request.form.get("email")
        if cur_email != new_email:
            _p1, _p2 = new_email.split("@")

            def check_p1_email(p_test, not_allowed):
                arr_test = [p_test.startswith(i) for i in not_allowed] + [p_test.endswith(i) for i in not_allowed]
                print(arr_test)
                return any(arr_test)

            if check_p1_email(_p1, "./@#_*&") or _p2.count('.') != 1:
                flash('Неправильный формат почты')
            else:
                cur_user.email = new_email

        file = request.files.get('file')
        if file.filename:
            available = ['png', 'jpg', 'jpeg']
            file_res = file.filename.split('.')[-1]
            if file_res not in available:
                flash('Формат файла не поддерживается')
            else:
                img_location = 'Site/static/img/profile_images'
                if not os.path.isdir(img_location):
                    os.mkdir(img_location)
                new_file = f'{img_location}/{secure_filename(f"{current_user.get_id()}.png")}'
                file.save(new_file)

        if request.form.get('show-select'):
            day, month, year = [int(request.form.get(key)) for key in ["Day", "Month", "Year"]]
            if all([day, month, year]) and 1 <= day <= 31 and 1 <= month <= 12 and 1898 <= year <= 2022:
                if day > 29 and month == 2 and year % 4:
                    day = 28
                cur_user.day = day
                cur_user.month = month
                cur_user.year = year
            else:
                flash('Неправильная новая дата рождения')

        if request.form.get('change-password'):
            cur_pass, new_pass, new_pass2 = [request.form.get(f"pass{i}") for i in range(3)]
            print(cur_pass, new_pass, new_pass2)
            if check_password_hash(cur_user.password, cur_pass):
                if cur_pass == new_pass:
                    flash('Пароль не может совпадать с текущим')
                else:
                    cur_user.password = generate_password_hash(new_pass)
                    print('gud')
            else:
                flash('Введенный пароль не совпадает с текущим')
        db.session.commit()

        return redirect(url_for('profile'))
    else:
        if superuser and superuser.admin_status == 2:
            try:
                cur_user = User.query.get(int(profile_id))
                if not cur_user:
                    cur_user = superuser
                    flash(f'Профиль с ID={profile_id} не существует')
            except ValueError:
                flash('Аргумент user_id должен быть числом!')
            except Exception as e:
                flash(e.__str__())
        p_image = url_for('static', filename=f'img/profile_images/{cur_user.id}.png')
        refs = ', '.join([user.login for user in User.query.filter_by(parent=cur_user.id).all()])
        refs = refs if refs else "У вас пока нет рефералов"
        current_orders = cur_user.current_orders if cur_user.current_orders else "У вас пока нет активных заказов"
        orders_id = cur_user.orders_id if cur_user.orders_id else "У вас пока нет завершенных заказов"
        try:
            birth = date(cur_user.year, cur_user.month, cur_user.day).strftime("%d.%m.%Y")
        except ValueError:
            birth = date(cur_user.year, cur_user.month, cur_user.day - 1).strftime("%d.%m.%Y")
            cur_user.day -= 1
            db.session.commit()
        if not os.path.exists("Site/" + p_image):
            p_image = DEFAULT_PROFILE_IMAGE
        return render_template('profile.html',
                               css=url_for('static', filename="css/profile.css"),
                               nickname=get_user_nick(),
                               user=cur_user,
                               profile_image=p_image,
                               birth=birth,
                               refs=refs,
                               ref_id=cur_user.id,
                               current_orders=current_orders,
                               completed_orders=orders_id)


@app.route('/apikey', methods=['GET', 'POST'])
@login_required
def apikey():
    user = User.query.get(current_user.get_id())
    user_api = Apikey.query.filter_by(requestor_id=user.id).first()
    if request.method == 'POST':
        if user_api:
            flash('У вас уже есть API ключ')
        else:
            create_apikey(user)
            return redirect(url_for('apikey'))
    return render_template('apikey.html', css=url_for('static', filename='css/apikey.css'),
                           user=user, apikey=user_api)


@app.route('/delete_apikey')
@login_required
def delete_apikey():
    user = User.query.get(current_user.get_id())
    Apikey.query.filter_by(requestor_id=user.id).delete()
    db.session.commit()
    return redirect(url_for('apikey'))


@app.route('/topup', methods=['GET', 'POST'])
@login_required
def topup():
    usr = User.query.get(current_user.get_id())
    _class = 'info'
    if request.method == 'POST':
        balance = request.form.get('money')
        if not balance:
            flash('Введите сумму пополнения')
        else:
            try:
                balance = round(float(balance), 2)
                if balance > 300000:
                    flash('Максимальная сумма пополнения - 300000')
                else:
                    _new = BalanceRequest(
                        login_for=usr.login,
                        sum=balance,
                        date=datetime.datetime.now().strftime('%d.%m.%Y.%H.%M.%S'),
                    )
                    db.session.add(_new)
                    db.session.commit()
                    _class = 'info-green'
                    flash('Заявка создана! Ждите решения администратора.')
            except ValueError:
                flash('Что-то пошло не так. Попробуйте ещё раз.')
    return render_template('topup.html', css=url_for('static', filename='css/topup.css'),
                           user=usr, info_class=_class)