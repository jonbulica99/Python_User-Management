import ZODB
from Persistence import Persistent
from utils.log import Logger

__version__ = 0.1


class BaseObject(Persistent):
    def __init__(self, name=self.__class__.__name__, version=__version__):
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized {0} v{1}".format(name, version))
