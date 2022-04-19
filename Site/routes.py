import os.path

from flask import render_template, url_for, request, redirect
from flask_login import login_required, current_user

from Site import app
from Site.models import User
from Site.settings import *


def get_user_nick():
    try:
        nick = User.query.get(current_user.get_id()).login
    except AttributeError:
        nick = None
    return nick


@app.route('/')
def index():
    ref = request.args.get("ref")
    if ref:
        return redirect(url_for('register', ref=ref))
    return render_template("index.html", css=url_for('static', filename='css/index.css'),
                           nickname=get_user_nick())


@app.route('/test')
def test():
    if not current_user.get_id():
        return redirect('login')

    return current_user.get_id()


@app.route('/profile', methods=["GET", 'POST'])
def profile():
    if not current_user.get_id():
        return redirect('login')

    if request.method == "POST":
        pass
    else:
        p_image = url_for('static', filename=f'img/profile_images/{current_user.get_id()}.png')
        if not os.path.exists("Site/" + p_image):
            p_image = DEFAULT_PROFILE_IMAGE
        return render_template('profile.html', css=url_for('static', filename="css/profile.css"),
                               nickname=get_user_nick(), profile_image=p_image)