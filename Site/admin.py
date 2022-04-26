from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from Site import app, db
from Site.models import User


@app.route('/admin')
def admin():
    user_id = current_user.get_id()
    if not user_id or User.query.get(user_id).admin_status != 2:
        return redirect(url_for('index'))
    return 'access'
