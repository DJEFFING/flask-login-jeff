import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "this_is_secret_key")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flask_login"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
