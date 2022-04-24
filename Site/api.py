from flask import jsonify
from flask_restful import reqparse, abort, Resource

from Site.models import User


def abort_if_user_not_found(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, message=f'User with id={user_id} not found')


class UsersResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('apikey', required=False)
        args = parser.parse_args()
        print(args.apikey)
        users = User.query.all()

        return jsonify([user.to_dict(only=('id', 'login',
                                           'day', 'month', 'year',
                                           'parent', 'balance',
                                           'orders_id', 'current_orders')) for user in users])


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        return jsonify({'status': 'ok'})
