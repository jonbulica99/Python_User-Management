import ZODB
from persistent import Persistent
from utils.log import Logger

__version__ = 0.1
__db_name__ = None


class BaseObject(Persistent):
    def __init__(self, name=None, version=__version__, db_name=__db_name__):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.db_name = db_name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s v%s", name, version)
