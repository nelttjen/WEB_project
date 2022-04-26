import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Resource

from Site.models import User, Apikey


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
