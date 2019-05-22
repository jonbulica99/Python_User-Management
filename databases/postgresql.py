from databases.mysql import Mysql


class Postgresql(Mysql):
    __version__ = 0.1
    default_port = 5432

    def __init__(self, database, *args, **kwargs):
        super().__init__(database, *args, **kwargs)
