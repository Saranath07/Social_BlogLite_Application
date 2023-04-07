import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DB_DIR = os.path.join(basedir, "/db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///project_example.sqlite3"
    DEBUG = True
    SECRET_KEY = "thisisasecretkey"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = "really super secret"
    #SECURITY_REGISTERABLE = True
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    