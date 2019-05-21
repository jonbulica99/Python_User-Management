from utils.log import Logger

__version__ = 0.1


class BaseObject(object):
    def __init__(self, name=None, version=__version__, *args, **kwargs):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
