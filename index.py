from Site.settings import *
from Site import app, config


if __name__ == '__main__':
    config.set('SECRET_KEY', SECRET_KEY)
    app.run(port=8080)
