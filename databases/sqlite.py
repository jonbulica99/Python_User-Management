from databases.sql_alchemy import SqlAlchemy

__version__ = 0.1

class Sqlite(SqlAlchemy):
    implementation = ""
    def __init__(self, database, *args, **kwargs):
        super().__init__(database=database, *args, **kwargs)
