from databases.sql_alchemy import SqlAlchemy

__version__ = 0.1

class Sqlite(SqlAlchemy):
    implementation = ""
    def __init__(self, database, version=__version__, *args, **kwargs):
        super().__init__(database=database, dialect="sqlite", version=version, *args, **kwargs)
