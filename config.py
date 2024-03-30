import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_very_secret_key')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    # Add development-specific configurations, like database URIs

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # Add testing-specific configurations

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Production configs like database URIs
    # Logging configurations
    # Security configurations, like SSL

# You can add more configurations for different environments as needed
