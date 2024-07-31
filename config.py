import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'vnkdjnfjknfl4568'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'chat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
