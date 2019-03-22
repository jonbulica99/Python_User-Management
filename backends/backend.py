from utils.log import Logger
from utils.decorators import notimplemented
from objects import *

__version__ = 0.1


class BaseBackend:
    def __init__(self, name=None, version=__version__, *args, **kwargs):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s backend v%s", name, version)
        self.connection = None

    def connect(self):
        self.log.debug("Connecting to %s backend v%s.", self.name, self.version)

    def close(self):
        self.log.debug("Closing connection to %s backend v%s.", self.name, self.version)
