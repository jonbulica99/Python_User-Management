from utils.log import Logger
from utils.decorators import notimplemented

from objects import *

__version__ = 0.1


class MethodBackend:
    add_user = None
    del_user = None
    en_user = None
    dis_user = None
    add_user_group = None
    del_user_group = None
    add_group = None
    del_group = None


class BaseBackend:
    def __init__(self, name=None, version=__version__, *args, **kwargs):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s backend v%s", name, version)
        self.db = None

    @notimplemented
    def connect(self):
        self.log.debug("Connecting to %s backend v%s.", self.name, self.version)

    @notimplemented
    def close(self):
        self.log.debug("Closing connection to %s backend v%s.", self.name, self.version)

    @notimplemented
    def sync_user(self, user: user.User):
        pass

    @notimplemented
    def sync_group(self, group: group.Group):
        pass
