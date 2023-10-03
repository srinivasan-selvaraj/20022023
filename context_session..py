from multiprocessing import get_logger
from queue import Queue
from config import ENVIRONMENT
from Wrappers.loggers import LogWrapper
from mongoengine import connect

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Session(object):
    _db = None
    _loggers = None
    _env = None
    session_queue = None

    def __init__(self, name):
        self.init()
        self.name = name
        self.session_queue = Queue()
        self._mapper = {}

    def init(self):
        self._env = ENVIRONMENT
        # Todo DB and logger init
        log = self._env['log']
        self._loggers = LogWrapper(log['level'], log['filename'], log['format'])
        self._db = connect(self._env['db']['name'], host=self._env['db']['host'], port=self._env['db']['port'],
                     username=self._env['db']['username'], password=self._env['db']['password'], authentication_source=self._env['db']['auth_source']
                    )
        self._loggers.info("Database is Connected")

    def get_logger(self):
        return self._loggers

    def get_db(self):
        self._db = connect(self._env['db']['name'], host=self._env['db']['host'], port=self._env['db']['port'],
                     username=self._env['db']['username'], password=self._env['db']['password'], authentication_source=self._env['db']['auth_source']
                    )
        self._loggers.info("Database is Connected")
        return self._db

    def get_env(self):
        return self._env

    def get_name(self):
        return self.name

    def get_session_queue(self):
        return self.session_queue

    def get_mapper(self):
        return self._mapper
