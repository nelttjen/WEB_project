from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from Site import app, db
from Site.models import User


def redirect_if_not_admin():
    user_id = current_user.get_id()
    if not user_id or User.query.get(user_id).admin_status != 2:
        return True
    return False


@app.route('/admin')
def admin():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr)


@app.route('/admin/topups')
def topups():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr,
                           current=1)


@app.route('/admin/users')
def users():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr,
                           current=2)


@app.route('/admin/boosters')
def boosters():
    if redirect_if_not_admin():
        return redirect(url_for('index'))
    usr = User.query.get(current_user.get_id())
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr,
                           current=3)


@app.route('/admin/orders')
def orders():
    redirect_if_not_admin()
    usr = User.query.get(current_user.get_id())
    return render_template('admin.html', css=url_for('static', filename='css/admin.css'), user=usr,
                           current=4)