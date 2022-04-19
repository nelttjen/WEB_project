from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from Site.Config import Config
from Site.settings import *

app = Flask(__name__)
config = Config(app)
config.set('SQLALCHEMY_DATABASE_URI',
           main_db)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from Site import models, auth, routes
