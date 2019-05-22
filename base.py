from utils.log import Logger


class BaseObject(object):
    __version__ = 0.1

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.log = Logger(name).get()
