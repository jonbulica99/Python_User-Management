import ZODB
from utils.log import Logger

__version__ = 0.1


class BaseDB:
    def __init__(self, name=None, version=__version__):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s v%s", name, version)
        self.db = None

    def connect(self):
        if self.db:
            try:
                self.connection = self.db.open()
                self.log.info("Established database connection to: %s", self.describe())
                return self.connection
            except Exception as e:
                self.log.error("Connection failure: %s", e)
        else:
            self.log.error("Failed to establish a valid database connection.")

    def describe(self):
        return self.name
