import ZODB.FileStorage
from databases.base import BaseDB

__version__ = 0.1


class FileDB(BaseDB):
    def __init__(self, file):
        super().__init__()
        self.path = file
        self.db = ZODB.DB(file)

    def describe(self):
        return "{} located at {}".format(self.name, self.path)
