from flask import Flask, render_template, url_for
from App.Config import Config
from App.settings import *

app = Flask(__name__)
config = Config(app)


@app.route('/')
def index():
    return render_template("base.html", css=url_for('static', filename='css/index.css'))


if __name__ == '__main__':
    config.set('SECRET_KEY', SECRET_KEY)
    print(config.get('SECRET_KEY'))
    app.run(port=8080)
