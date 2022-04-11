from flask import render_template, url_for, request, redirect
from flask_login import login_required

from Site import app


@app.route('/')
def index():
    return render_template("base.html", css=url_for('static', filename='css/index.css'))


@app.route('/test')
@login_required
def test():
    return "logged"