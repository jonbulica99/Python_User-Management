from databases.sql_alchemy import SqlAlchemy

__version__ = 0.1

class Mysql(SqlAlchemy):
    implementation = "{user}:{pwd}@{host}:{port}"
    def __init__(self, database, user, pwd, host, port=3306, version=__version__):
        super().__init__(database=database, version=version)
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
