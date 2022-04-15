from flask import render_template, url_for, request, redirect
from flask_login import login_required, current_user

from Site import app
from Site.models import User


@app.route('/')
def index():
    return render_template("index.html", css=url_for('static', filename='css/index.css'),
                           nickname=User.query.get(current_user.get_id()).login)


@app.route('/test')
@login_required
def test():
    return current_user.get_id()


@app.route('/test2')
def test2():
    message = "1"
    return render_template("test.html", message=message)