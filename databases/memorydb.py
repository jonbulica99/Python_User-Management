from databases.filedb import FileDB

__version__ = 0.1


class MemoryDB(FileDB):
    def __init__(self):
        super().__init__(None)

    def describe(self):
        return "In-Memory database"
