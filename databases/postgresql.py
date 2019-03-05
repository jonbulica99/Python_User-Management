from databases.mysql import Mysql

__version__ = 0.1

class Postgresql(Mysql):
    def __init__(self, database, user, pwd, host, port=5432, version=__version__, *args, **kwargs):
        super().__init__(database, user, pwd, host, port=port, version=version, *args, **kwargs)
