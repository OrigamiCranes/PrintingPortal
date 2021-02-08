import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'example-key'

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/database"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = 86400

    TESTING = False
    LOGIN_DISABLED = False
    WTF_CSRF_ENABLED = True


class Test(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/database-test"

    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False

