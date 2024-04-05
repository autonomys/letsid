# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_very_secret_key')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 'development'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False