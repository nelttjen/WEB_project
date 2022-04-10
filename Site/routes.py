from flask import render_template, url_for, request

from Site import app


@app.route('/')
def index():
    return render_template("base.html", css=url_for('static', filename='css/index.css'))