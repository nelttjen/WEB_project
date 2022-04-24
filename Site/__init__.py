import js2py
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from Site.config import Config
from Site.settings import *

app = Flask(__name__)
config = Config(app)
config.set('SQLALCHEMY_DATABASE_URI',
           main_db)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
generate_API = js2py.eval_js(open('data/generateAPI.js').read())

from Site import models, auth, routes