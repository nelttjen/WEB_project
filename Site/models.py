from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from Site import db


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, default="")
    password = db.Column(db.String, nullable=False)

    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    parent = db.Column(db.Integer, default=-1)

    balance = db.Column(db.Float, default=0)
    orders_id = db.Column(db.String, default="")
    current_orders = db.Column(db.String, default="")

    admin_status = db.Column(db.Integer, default=0)
    is_banned = db.Column(db.Float, default=False)
    until = db.Column(db.String, default="")


class Booster(db.Model, UserMixin):
    __tablename__ = 'booster'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    output_balance = db.Column(db.Float, default=0)
    boost_orders_id = db.Column(db.String)
    current_boost_orders = db.Column(db.String)


class Apikey(db.Model):
    __tablename__ = 'apikeys'

    id = db.Column(db.Integer, primary_key=True)
    apikey = db.Column(db.String, unique=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    info = db.Column(db.String)
    access_level = db.Column(db.Integer, nullable=False)

    # access levels:
    # 1 - moderator
    # 2 - administrator
    # 99 - full, autogenerate

    creation_date = db.Column(db.String, nullable=False)
    valid_end = db.Column(db.String, nullable=False)
