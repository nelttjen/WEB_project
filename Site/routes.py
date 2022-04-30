import datetime
import os.path
import random
import string

import js2py
from flask import render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from datetime import date

from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from Site import app, db
from Site.models import User, Apikey, BalanceRequest, Promo, ApexOrder, Booster
from Site.settings import *
from Site.api import create_apikey


def get_user_nick():
    try:
        nick = User.query.get(current_user.get_id()).login
    except AttributeError:
        nick = None
    return nick


_promo_check_last = datetime.datetime(2000, 11, 11, 11, 11, 11)


def check_everyday_promo(force=False):
    global _promo_check_last
    _delta = datetime.datetime.now() - _promo_check_last
    if _delta.seconds + (_delta.days * 3600 * 24) > 3600 or force:
        _promo_check_last = datetime.datetime.now()
        promo = Promo.query.filter_by(type=0).first()
        if not promo:
            update_everyday_promo()
        else:
            d, m, y, H, M, S = map(int, promo.creation_date.split('.'))
            created = datetime.datetime(y, m, d, H, M, S)
            promo_delta = datetime.datetime.now() - created
            if promo_delta > datetime.timedelta(seconds=int(promo.valid_hours) * 60 * 60):
                update_everyday_promo()


def update_everyday_promo():
    promos = Promo.query.filter_by(type=0).all()
    if promos:
        for i in promos:
            db.session.delete(i)
        db.session.commit()
    _new = Promo(
        code=''.join(random.sample(string.ascii_letters + string.digits, 7)),
        uses_left=10,
        discount=33,
        creation_date=datetime.datetime.now().strftime('%d.%m.%Y.%H.%M.%S'),
        valid_hours=24,
        type=0
    )
    db.session.add(_new)
    db.session.commit()


def calculate_sum_order(rank1, rank2):
    calc_sum = js2py.eval_js(open('data/calc_sum.js').read())
    return calc_sum(rank1, rank2)


def calculate_with_promo(price, promo, ret_promo=False):
    if isinstance(promo, Promo):
        promo = promo.code
    if not promo:
        if ret_promo:
            return price, promo
        return price
    check_everyday_promo(force=True)
    _promo = Promo.query.filter_by(code=promo).first()
    if _promo and _promo.uses_left > 0:
        price = price - price * (_promo.discount / 100)
    if ret_promo:
        return price, _promo
    return price


def get_curr_user():
    return User.query.get(current_user.get_id())


@app.route('/')
@app.route('/index')
def index():
    check_everyday_promo()
    ref = request.args.get("ref")
    if ref:
        return redirect(url_for('register', ref=ref))
    promo = Promo.query.filter_by(type=0).first()
    return render_template("index.html",
                           css=url_for('static', filename='css/index.css'),
                           user=get_curr_user(),
                           promo=promo)


# @app.route('/test')
# def test():
#     _delta = datetime.datetime.now() - launch
#     h, m, s = str(_delta).split(', ')[1].split(':') if str(_delta).count(',') > 0 else str(_delta).split(':')
#     stack = [int(_delta.days), int(h), int(m), int(float(s))]
#     return f'{int(_delta.days)} days, {int(h)} hours, {int(m)} minutes, {int(float(s))} seconds'


@app.route('/profile', methods=["GET", 'POST'])
@login_required
def profile():
    profile_id = request.args.get('user_id')
    superuser = None
    cur_user = get_curr_user()
    if profile_id:
        superuser = cur_user
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
                               balance=round(cur_user.balance, 2),
                               profile_image=p_image,
                               birth=birth,
                               refs=refs,
                               ref_id=cur_user.id,
                               current_orders=current_orders,
                               completed_orders=orders_id)


@app.route('/apikey', methods=['GET', 'POST'])
@login_required
def apikey():
    user = get_curr_user()
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
    user = get_curr_user()
    Apikey.query.filter_by(requestor_id=user.id).delete()
    db.session.commit()
    return redirect(url_for('apikey'))


@app.route('/topup', methods=['GET', 'POST'])
@login_required
def topup():
    usr = get_curr_user()
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
                elif balance <= 0:
                    flash('Сумма пополнения должна быть больше 0')
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
                           user=usr,
                           balance=round(usr.balance, 2),
                           info_class=_class)


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    check_everyday_promo()
    usr = get_curr_user()
    promo = Promo.query.filter_by(type=0).first()
    if request.method == "POST":
        try:
            rank1 = int(request.form.get('from-input'))
            rank2 = int(request.form.get('to-input'))
            _log = request.form.get('order_1')
            _pas = request.form.get('order_2')
            assert _log and _pas
            assert rank2 > rank1
            assert 0 <= rank1 <= 20000 and 0 <= rank2 <= 20000
            _sum = calculate_sum_order(rank1, rank2)
            _hours = rank2 - rank1 // 100
            _promo = request.form.get('code')
            _order_confirm_code = ''.join(random.sample(string.ascii_letters, 32))
            _new = ApexOrder(
                requestor_id=usr.id,
                account=f"{_log}:{_pas}",
                status=-1,
                confirm_code=_order_confirm_code,
                used_promo=_promo,
                from_points=rank1,
                to_points=rank2,
                price=_sum,
                date_created=datetime.datetime.now().strftime('%d.%m.%Y.%H.%M.%S'),
            )
            db.session.add(_new)
            db.session.commit()
            return redirect(url_for('confirm', order_code=_order_confirm_code))
        except (ValueError, AssertionError):
            flash('Что-то пошло не так. Попробуйте ещё раз.')

    return render_template('order.html', css=url_for('static', filename='css/order.css'),
                           user=usr, promo=promo)


@app.route('/order/confirm')
@login_required
def confirm():
    check_everyday_promo()
    usr = get_curr_user()
    order_code = request.args.get('order_code')
    if not order_code:
        return redirect(url_for('order'))
    _order = ApexOrder.query.filter_by(confirm_code=order_code).first()
    if not _order or _order.status != -1:
        flash('Заказ не найден')
        return redirect(url_for('order'))
    promo = _order.used_promo
    _promo = None
    if promo:
        _promo = Promo.query.filter_by(code=promo).first()
        if not _promo or _promo.uses_left <= 0:
            _promo = None
    price1 = round(_order.price, 2)
    price2 = 0
    if _promo:
        price2, _promo = calculate_with_promo(_order.price, _promo, ret_promo=True)
    return render_template('order_confirm.html', css=url_for('static', filename='css/order.css'),
                           user=usr, promo=None, used_promo=_promo, order=_order,
                           price1=price1, price2=price2)


@app.route('/order/confirm/<string:order_id>')
@login_required
def confirm_by_id(order_id):
    action = request.args.get('action')
    usr = get_curr_user()
    if not action or action not in ('accept', 'reject'):
        flash('Неизвестное действие')
        return redirect(url_for('order'))
    _order = ApexOrder.query.filter_by(confirm_code=order_id).first()
    if not _order or _order.status != -1 or (_order.requestor_id != usr.id and usr.admin_status < 2):
        flash('Заказ не найден')
        return redirect(url_for('order'))
    if action == 'accept':
        price = _order.price
        _promo = None
        if _order.used_promo:
            price, _promo = calculate_with_promo(price, _order.used_promo, ret_promo=True)
        if usr.balance >= price:
            _order.price = round(price, 2)
            usr.balance = round(usr.balance - price, 2)
            _order.status = 0
            if _promo and _promo.uses_left > 0:
                _promo.uses_left -= 1
            db.session.commit()
            flash('Заказ создан! Ожидайте принятия одним из наших бустеров!', 'succ')
            return redirect(url_for('myorders'))
        else:
            flash('Недостаточно средств на балансе. Пожалуйста, пополните баланс')
            return redirect(url_for('topup'))
    else:
        db.session.delete(_order)
        db.session.commit()
        flash('Заказ отменен', 'succ')
        return redirect(url_for('order'))


@app.route('/profile/myorders')
@login_required
def myorders():
    usr = get_curr_user()
    orders = ApexOrder.query.filter_by(requestor_id=usr.id).all()
    return render_template('myorders.html', css=url_for('static', filename='css/myorders.css'),
                           orders=orders, user=usr)


@app.route('/profile/myorders/order')
def order_action():
    usr = get_curr_user()
    action = request.args.get('action')
    _order = ApexOrder.query.filter_by(confirm_code=request.args.get('order_code')).first()
    if action not in ('confirm', 'cancel'):
        flash('Недостаточно аргументов')
        return redirect(url_for('myorders'))
    if not _order or _order.requestor_id != usr.id:
        flash('Заказ не найден')
        return redirect(url_for('myorders'))
    if action == 'confirm':
        if _order.status == 2:
            _order.status = 3
            booster = Booster.query.filter_by(user_id=_order.booster_id).first()
            if booster:
                booster.output_balance += round(order.price, 2)
            db.session.commit()
            flash('Выполнение заказа подтверждено! Деньги отправлены исполнителю.', 'succ')
        else:
            flash('Что-то пошло не так, попробуйте ещё раз')
    else:
        if _order.status == 0:
            _order.status = 4
            usr.balance += round(_order.price, 2)
            db.session.commit()
            flash('Заказ отменен. Деньги возвращены на баланс.', 'succ')
        else:
            flash('Что-то пошло не так, попробуйте ещё раз')
    return redirect(url_for('myorders_id', order_id=_order.id))


@app.route('/profile/myorders/order/<int:order_id>')
@login_required
def myorders_id(order_id):
    usr = get_curr_user()
    _order = ApexOrder.query.filter_by(id=order_id).first()
    if not _order or _order.requestor_id != usr.id:
        flash('Заказ не найден')
        return redirect(url_for('myorders'))
    return render_template('myorders_show.html',
                           css=url_for('static', filename='css/myorders.css'),
                           order=_order, user=usr
                           )
