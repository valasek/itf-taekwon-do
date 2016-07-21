import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///itf_alchemy_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///itf_alchemy_dev_db.db'
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///itf_alchemy_test_db.db'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///itf_alchemy_test_db.db'
    SECRET_KEY = '792842bc-c4df-4de1-9177-d5207bd9faa6'

config = {
    "dev": "config.DevelopmentConfig",
    "test": "config.TestingConfig",
    "default": "config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.logger.debug("Loaded configuration: %s", config[config_name])
    #app.config.from_pyfile('config.py', silent=True)
