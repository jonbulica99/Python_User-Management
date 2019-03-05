from enum import Enum
from pydoc import locate
from utils.extras import safeformat

class DbType(Enum):
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MEMORY = "memory"
    POSTGRESQL = "postgresql"


class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.type = DbType(self.setting("type"))

    def setting(self, setting):
        return self.db_config.get(setting)

    def setup_database(self):
        import_string = "databases.{module}.{cls}"
        SqlAlchemyImpl = locate(import_string.format(module=self.type.value.lower(), cls=self.type.value.title()))
        return SqlAlchemyImpl(**self.db_config)

    def create_database(self, db_type, db_config={}):
        self.type = DbType(db_type)
        if db_config or self.type == DbType.MEMORY:
            self.db_config = db_config
        return self.setup_database()

    @staticmethod
    def db_supported_types():
        return [t for t in DbType]
