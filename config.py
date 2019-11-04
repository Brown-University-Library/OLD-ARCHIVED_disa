import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
print( f'ABC123 -- in config.py, basedir, ```{basedir}```' )

load_dotenv(os.path.join(basedir, '.envrc'))

class Config(object):
    APP_DIR = basedir
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
