from flask import Flask
from flask_login import LoginManager

from Site.Config import Config

app = Flask(__name__)
config = Config(app)
login_manager = LoginManager(app)

from Site import models, auth, routes
