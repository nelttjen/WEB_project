class Config:
    def __init__(self, app):
        self.app = app

    def set(self, key, val):
        self.app.config[key] = val

    def get(self, key):
        try:
            return self.app.config[key]
        except:
            return
