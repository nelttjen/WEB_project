import datetime
import os
import requests

from flask import url_for, render_template, request, flash
from flask_login import current_user
from werkzeug.utils import redirect
from urllib.parse import urlparse, urljoin

from Site import app, launch
from Site.models import *
from Site.api import create_apikey, get_and_check_apikey


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_if_not_admin():
    user_id = current_user.get_id()
    if not user_id or User.query.get(user_id).admin_status != 2:
        return True
    return False


def check_apikey(user):
    apikey = Apikey.query.filter_by(requestor_id=user.id).first()
    if not apikey:
        create_apikey(user)
    else:
        _, valid, ___ = get_and_check_apikey(apikey.apikey)
        if not valid:
            db.session.delete(apikey)
            create_apikey(user)
            db.session.commit()


def get_deltatime(_from, _to):
    _delta = _to - _from
    h, m, s = str(_delta).split(', ')[1].split(':') if str(_delta).count(',') > 0 else str(_delta).split(':')
    return [int(_delta.days), int(h), int(m), int(float(s))]


@app.route('/admin')
def admin():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    total_users = User.query.all()
    total_topup = BalanceRequest.query.filter_by(accepted=0).all()
    total_apikeys = Apikey.query.all()
    active_orders = ApexOrder.query.filter_by(status=2).all()
    completed_orders = ApexOrder.query.filter_by(status=3).all()
    total_boosters = Booster.query.all()
    total_orders_sum = ApexOrder.query.filter(ApexOrder.status != 4 and
                                              ApexOrder.status != 5 and
                                              ApexOrder.status != -1).all()
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr,
                           time=get_deltatime(launch, datetime.datetime.now()),
                           total_users=len(total_users), total_topup=len(total_topup),
                           active_orders=len(active_orders), completed_orders=len(completed_orders),
                           total_boosters=len(total_boosters),
                           total_orders_sum=round(sum([i.price for i in total_orders_sum]), 2),
                           total_apikeys=len(total_apikeys), info_class='info'
                           )


@app.route('/admin/topups')
def topups():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    check_apikey(usr)
    return render_template('admin_topups.html', css=url_for('static', filename='css/admin_topups.css'), user=usr,
                           current=1, requests=BalanceRequest.query.filter(BalanceRequest.accepted == 0).all(),
                           apikey=Apikey.query.filter_by(requestor_id=usr.id).first().apikey,

                           info_class='info')


@app.route('/admin/users')
def users():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    check_apikey(usr)
    return render_template('admin_users.html', css=url_for('static', filename='css/admin_users.css'), user=usr,
                           current=2, info_class='info')


@app.route('/admin/boosters')
def boosters():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    check_apikey(usr)
    return render_template('admin_boosters.html', css=url_for('static', filename='css/admin_boosters.css'), user=usr,
                           current=3, info_class='info')


@app.route('/admin/orders')
def orders():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    check_apikey(usr)
    return render_template('admin_orders.html', css=url_for('static', filename='css/admin_orders.css'), user=usr,
                           current=4, info_class='info')


@app.route('/admin/request')
def _request():

    def get_next(__next):
        if __next and __next in ('orders', 'boosters', 'users', 'topups'):
            return __next
        return 'admin'

    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    port = os.environ.get('PORT', 8080)
    _next = request.args.get('next')
    req_type = request.args.get('type')
    apikey = request.args.get('apikey')
    if not req_type or not apikey:
        flash('Недостаточно параметров запроса', category='fail')
        return redirect(url_for(get_next(_next)))
    else:
        if req_type == 'balance':
            req_id = request.args.get('request_id')
            action = request.args.get('action')
            if not req_id or not action:
                flash('Недостаточно параметров запроса', category='fail')
                return redirect(url_for(get_next(_next)))
            resp = requests.post(f'http://localhost:{port}/api/v1.0/accept/balance_request'
                                 f'?apikey={apikey}&action={action}'
                                 f'&request_id={req_id}&acceptor_id={usr.id}').json()
            if resp['message'] == 'OK':
                msg = f'Заявка успешно {"принята" if resp["action"] == "accept" else "отклонена"}' \
                    if req_id != 'all' else 'Все заявки успешно ' \
                                            f'{"приняты" if resp["action"] == "accept" else "отклонены"}'
                flash(msg, 'succ')
            else:
                flash(resp['message'], 'fail')
            return redirect(url_for(get_next(_next)))