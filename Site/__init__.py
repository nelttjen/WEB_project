from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from Site.Config import Config

app = Flask(__name__)
config = Config(app)
config.set('SQLALCHEMY_DATABASE_URI',
           'sqlite:///C:\\Users\\Home2\\PycharmProjects\\Projects\\WEB_project\\data\\newDB.db')
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from Site import models, auth, routes
