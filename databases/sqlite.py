from databases.sql_alchemy import SqlAlchemy

__version__ = 0.1

class Sqlite(SqlAlchemy):
    def __init__(self, file, version=__version__):
        super().__init__(database=file, dialect="sqlite", version=version)
        self.conn_data = {
            "dialect": self.dialect,
            "database": self.database
        }
        connection_string = "{dialect}:///{database}"
        self.connect(implementation=connection_string.format(**self.conn_data))
