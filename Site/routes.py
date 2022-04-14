from flask import render_template, url_for, request, redirect
from flask_login import login_required, current_user

from Site import app


@app.route('/')
def index():
    return render_template("index.html", css=url_for('static', filename='css/index.css'))


@app.route('/test')
@login_required
def test():
    return current_user.get_id()