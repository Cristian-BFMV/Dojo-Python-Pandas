from gunicorn.http import wsgi
# config.py

class Response(wsgi.Response):
    def default_headers(self, *args, **kwargs):
        headers = super(Response, self).default_headers(*args, **kwargs)
        return [h for h in headers if not h.startswith('Server:')]

wsgi.Response = Response

class Config(object):
    """
    Common configurations
    """

    import gunicorn

    gunicorn.SERVER_SOFTWARE = 'Microsoft-IIS/6.0'

    PLATFORM_ENVIRONMENTS = ['accounting']


class DevelopmentConfig(Config):
    """
    Development configurations change
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    SERVER_PREFIX = 'http://localhost:8000'
    EMAIL_DOMAIN = '@t.t'
    LOG_PATH = '../logs/'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    SERVER_PREFIX = 'http://localhost:8000'
    EMAIL_DOMAIN = '@t.com.co'
    LOG_PATH = '../logs/'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
