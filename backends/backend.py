from base import BaseObject
from utils.decorators import notimplemented
from objects import *

__version__ = 0.1


class BaseBackend(BaseObject):
    def __init__(self, name=None, version=__version__, *args, **kwargs):
        super().__init__(name, version, *args, **kwargs)
        self.log.debug("Initialized %s backend v%s", name, version)
        self.connection = None

    def connect(self):
        self.log.debug("Connecting to %s backend v%s.", self.name, self.version)

    def close(self):
        self.log.debug("Closing connection to %s backend v%s.", self.name, self.version)
