from base import BaseObject
from utils.decorators import notimplemented
from objects import *


class BaseBackend(BaseObject):
    __version__ = 0.1

    def __init__(self, name=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.log.debug("Initialized %s backend v%s", name, self.__version__)
        self.connection = None

    def connect(self):
        self.log.debug("Connecting to %s backend v%s.",
                       self.name, self.__version__)

    def close(self):
        self.log.debug("Closing connection to %s backend v%s.",
                       self.name, self.__version__)
