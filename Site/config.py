class Config:
    def __init__(self, app):
        self.app = app

    def set(self, key, val):
        self.app.config[key] = val

    def get(self, key):
        return self.app.config.get(key)