import argparse
import os

from werkzeug.security import generate_password_hash

from Site import API, app, db, generate_API
from Site.settings import *
from Site.api import *
from Site.models import Apikey

if __name__ == '__main__':
    db.create_all()
    API.add_resource(UsersResource, APIROUTE + "/users")
    API.add_resource(UserResource, APIROUTE + "/users/<int:user_id>")
    API.add_resource(BalanceAccept, APIROUTE + '/accept/balance_request')
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-superuser', action='store_true')
    parser.add_argument('--create-superapi', action='store_true')
    parser.add_argument('--get-superapi', action='store_true')
    args = parser.parse_args()
    if args.create_superuser:
        log = input('Логин: ')
        psw = input('Пароль: ')
        usr = User(
            login=log,
            password=generate_password_hash(psw),
            day=1, month=1, year=1,
            admin_status=2
        )
        db.session.add(usr)
        db.session.commit()
    if args.create_superapi:
        date = datetime.datetime.now().strftime('%d.%m.%Y')
        api = generate_API()
        new_api = Apikey(apikey=api, requestor_id=0,
                         info="Autocreated superApi",
                         access_level=99, creation_date=date,
                         valid_end='Unlimited')
        db.session.add(new_api)
        db.session.commit()
    if args.get_superapi:
        print([i.apikey for i in Apikey.query.filter_by(access_level=99).all()])
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
