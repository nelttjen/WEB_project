import argparse

from werkzeug.security import generate_password_hash

from Site.settings import *
from Site import app, config, db
from Site.models import User

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-superuser', action='store_true')
    args = parser.parse_args()
    db.create_all()
    config.set('SECRET_KEY', SECRET_KEY)
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

    app.run(port=8080)
