from flask_login import UserMixin

from Site import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    parent = db.Column(db.Integer, default=-1)
    referals = db.Column(db.String)

    balance = db.Column(db.Float, default=0)
    orders_id = db.Column(db.String)
    current_orders = db.Column(db.String)

    account_type = db.Column(db.Integer, nullable=False)