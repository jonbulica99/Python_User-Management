from databases.sql_alchemy import SqlAlchemy

__version__ = 0.1

class Sqlite(SqlAlchemy):
    def __init__(self, file, version=__version__):
        super().__init__(database=file, dialect="sqlite", version=version)
