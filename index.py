from Site.settings import *
from Site import app, config, db

if __name__ == '__main__':
    db.create_all()
    config.set('SECRET_KEY', SECRET_KEY)
    app.run(port=8080)
