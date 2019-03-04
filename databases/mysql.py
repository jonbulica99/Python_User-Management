from databases.sql_alchemy import SqlAlchemy

__version__ = 0.1

class Mysql(SqlAlchemy):
    def __init__(self, database, user, pwd, host, port=3306, version=__version__):
        super().__init__(database=database, dialect="mysql", version=version)
        self.conn_data = {
            "dialect": self.dialect,
            "user": user,
            "pwd": pwd,
            "host": host,
            "port": port,
            "database": self.database
        }
        connection_string = "{dialect}://{user}:{pwd}@{host}:{port}/{database}"
        self.connect(implementation=connection_string.format(**self.conn_data))