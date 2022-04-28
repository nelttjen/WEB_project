import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Resource

from Site import generate_API, db
from Site.settings import APIKEY_DAYS_VALID
from Site.models import User, Apikey, BalanceRequest


def abort_if_user_not_found(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, message=f'User with id={user_id} not found', response=None, status='404')


def get_and_check_apikey(apikey):
    valid = False
    apikey = Apikey.query.filter_by(apikey=apikey).first()
    message = ''
    if apikey:
        valid = True
        if apikey.valid_end != 'Unlimited':
            d, m, y = map(int, apikey.valid_end.split('.'))
            date1 = datetime.date.today()
            date2 = datetime.date(y, m, d)
            if date2 < date1:
                valid = False
                message = f'Your Apikey expired {date2.strftime("%d.%m.%Y")}. Please, update your Apikey!'
    return apikey, valid, message


def create_apikey(user):
    c_date = datetime.datetime.now().strftime('%d.%m.%Y')
    e_date = datetime.datetime.now() + datetime.timedelta(days=APIKEY_DAYS_VALID)
    e_date = e_date.strftime('%d.%m.%Y')
    new_apikey = generate_API()
    req_id = user.id
    access_level = user.admin_status
    info = f'''User id {user.id} with access level {
    ["User", "Moderator", "Administrator"][user.admin_status]}'''
    _apikey = Apikey(apikey=new_apikey,
                     requestor_id=req_id,
                     info=info,
                     access_level=access_level,
                     creation_date=c_date,
                     valid_end=e_date)
    db.session.add(_apikey)
    db.session.commit()


def get_allowed_fields(level):
    basic = ['id', 'login', 'parent', 'current_orders']
    if level == 99:
        return ('id', 'login',
                'day', 'month', 'year',
                'parent', 'balance',
                'orders_id', 'current_orders', 'password')
    elif level == 1:
        basic += ['day', 'month', 'year']
    elif level == 2:
        basic += ['day', 'month', 'year', 'balance', 'orders_id', 'current_orders']
    return basic


class UsersResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('apikey', required=False)
        args = parser.parse_args()
        users = User.query.all()
        allowed = ['id', 'login', 'parent', 'current_orders']
        access_level = 0
        message = 'OK'
        if args.apikey:
            apikey, valid, msg = get_and_check_apikey(args.apikey)
            if valid:
                allowed = get_allowed_fields(apikey.access_level)
                access_level = apikey.access_level
            elif not apikey:
                message = 'Apikey is invalid!'
            else:
                message = msg
        response = {
            'response': [user.to_dict(only=allowed) for user in users if user.admin_status <= access_level],
            'message': message,
            'status': '200'
        }
        return jsonify(response)


class UserResource(Resource):
    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('apikey', required=False)
        args = parser.parse_args()
        valid = False
        apikey, message, allowed = [None] * 3
        if args.apikey:
            apikey, valid, msg = get_and_check_apikey(args.apikey)
            if valid:
                allowed = get_allowed_fields(apikey.access_level)
            elif not apikey:
                message = 'Apikey is invalid!'
            else:
                message = msg
        else:
            message = 'Apikey is required!'
        user = User.query.get(user_id)
        if not valid:
            response = {
                'response': None,
                'message': message,
                'status': '401'
            }
        else:
            abort_if_user_not_found(user_id)
            if user.admin_status <= apikey.access_level:
                response = {
                    'response': user.to_dict(only=allowed),
                    'message': f'User with id {user_id}, access level: '
                               f'''{["User", "Moderator", "Administrator"][apikey.access_level] 
                               if apikey.access_level != 99 else "Superuser"}''',
                    'status': '200'
                }
            else:
                response = {
                    'response': None,
                    'message': 'Your access level is too low to show this user',
                    'status': '401'
                }
        return jsonify(response)


class BalanceAccept(Resource):
    def get(self):
        return jsonify({'message': "method not allowed"})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('apikey', required=True)
        parser.add_argument('request_id', required=True)
        parser.add_argument('acceptor_id', required=True)
        args = parser.parse_args()
        if not args.apikey or not args.request_id or not args.acceptor_id:
            return abort(401, message='Not enough params')
        apikey, valid, msg = get_and_check_apikey(args.apikey)

        def accept_request(request, a_id):
            request.accepted = 1
            request.acceptor_id = a_id
            _sum = request.sum
            usr = User.query.filter_by(login=request.login_for).first()
            if not usr:
                return
            else:
                usr.balance += _sum
                if usr.parent != -1:
                    usr2 = User.query.get(usr.parent)
                    usr2.balance += round(_sum / 10, 2)
        if apikey.access_level >= 2:
            if args.get('request_id') == 'all':
                for req in BalanceRequest.query.filter(BalanceRequest.accepted == 0).all():
                    accept_request(req, int(args.acceptor_id))
            else:
                _id = args.get('request_id')
                accept_request(BalanceRequest.query.filter_by(id=_id).first(), int(args.acceptor_id))
            db.session.commit()
            return jsonify({'message': 'OK'})
        else:
            abort(401, message='Apikey access level is to low')