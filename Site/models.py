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


class Booster(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'booster'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    output_balance = db.Column(db.Float, default=0)
    boost_orders_id = db.Column(db.String)
    current_boost_orders = db.Column(db.String)


class Apikey(db.Model, SerializerMixin):
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


class ConfirmCode(db.Model, SerializerMixin):
    __tablename__ = 'recovery_codes'

    id = db.Column(db.Integer, primary_key=True)
    login_for = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    creation = db.Column(db.String, nullable=False)
    valid_mins = db.Column(db.String, nullable=False, default=30)


class BalanceRequest(db.Model, SerializerMixin):
    __tablename__ = 'balance_reqs'
    id = db.Column(db.Integer, primary_key=True)
    login_for = db.Column(db.String, nullable=False)
    sum = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)

    # accepted
    # -1 = rejected
    # 0 = pending
    # 1 - accepted

    accepted = db.Column(db.Float, nullable=False, default=False)
    acceptor_id = db.Column(db.Integer, default=-1)


class ApexOrder(db.Model, SerializerMixin):
    __tablename__ = 'apex_orders'
    id = db.Column(db.Integer, primary_key=True)

    requestor_id = db.Column(db.Integer, nullable=False)
    booster_id = db.Column(db.Integer, default=-1)

    account = db.Column(db.String, nullable=False)

    status = db.Column(db.Integer, default=0)
    # statuses
    # 0 - created
    # 1 - accepted
    # 2 - in_progress
    # 3 - done
    # 4 - canceled
    # 5 - banned

    from_points = db.Column(db.Integer, nullable=False)
    to_points = db.Column(db.Integer, nullable=False)
    addons = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)

    date_created = db.Column(db.String, nullable=False)
    date_accepted = db.Column(db.String)
    date_in_progress = db.Column(db.String)
    date_done = db.Column(db.String)
    date_canceled = db.Column(db.String)
    date_banned = db.Column(db.String)

    info = db.Column(db.String)


class Promo(db.Model, SerializerMixin):
    __tablename__ = 'promocodes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    uses_left = db.Column(db.Integer, nullable=False, default=10)
    discount = db.Column(db.Integer, nullable=False)

    creation_date = db.Column(db.String, nullable=False)
    valid_hours = db.Column(db.String, nullable=False, default=24)

    type = db.Column(db.Integer, nullable=False)
    # types
    # 0 - everyday
    # 1 - private

