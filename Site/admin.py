import datetime

from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from Site import app, db, launch
from Site.models import User
from Site.routes import create_apikey


def redirect_if_not_admin():
    user_id = current_user.get_id()
    if not user_id or User.query.get(user_id).admin_status != 2:
        return True
    return False


def get_time():
    _delta = datetime.datetime.now() - launch
    h, m, s = str(_delta).split(', ')[1].split(':') if str(_delta).count(',') > 0 else str(_delta).split(':')
    return [int(_delta.days), int(h), int(m), int(float(s))]


@app.route('/admin')
def admin():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr,
                           time=get_time())


@app.route('/admin/topups')
def topups():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin_topups.html', css=url_for('static', filename='css/admin_topups.css'), user=usr,
                           current=1)


@app.route('/admin/users')
def users():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin_users.html', css=url_for('static', filename='css/admin_users.css'), user=usr,
                           current=2)


@app.route('/admin/boosters')
def boosters():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin_boosters.html', css=url_for('static', filename='css/admin_boosters.css'), user=usr,
                           current=3)


@app.route('/admin/orders')
def orders():
    redirect_if_not_admin()
    usr = User.query.get(current_user.get_id())
    return render_template('admin_orders.html', css=url_for('static', filename='css/admin_orders.css'), user=usr,
                           current=4)