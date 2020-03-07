import logging
import logging.handlers as handlers
import os


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# python 3 style
class MyLogger(object, metaclass=SingletonType):
    # __metaclass__ = SingletonType   # python 2 Style
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("")
        self._logger.setLevel(logging.DEBUG)

    def init_app(self, app):
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')
        dirname = app.config['LOG_PATH']

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        errorLogHandler = handlers.RotatingFileHandler(dirname + 'alertaccounts_error.err', mode='w', maxBytes=100000000, backupCount=5)
        errorLogHandler.setFormatter(formatter)
        errorLogHandler.setLevel(logging.ERROR)
        self._logger.addHandler(errorLogHandler)

        fileHandler = handlers.RotatingFileHandler(dirname + 'alertaccounts_info.log', mode='w', maxBytes=100000000, backupCount=5)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(logging.INFO)
        self._logger.addHandler(fileHandler)

        print("Generate new instance")

    def get_logger(self):
        return self._logger
