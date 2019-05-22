from databases.sql_alchemy import SqlAlchemy


class Mysql(SqlAlchemy):
    __version__ = 0.1
    implementation = "{user}:{pwd}@{host}:{port}"
    default_port = 3306

    def __init__(self, database, *args, **kwargs):
        super().__init__(database=database, *args, **kwargs)
        self.user = kwargs.get('user')
        self.pwd = kwargs.get('pwd')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', self.default_port)
