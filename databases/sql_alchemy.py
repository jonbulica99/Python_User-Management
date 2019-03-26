from sqlalchemy import create_engine, select, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from databases.base import BaseDB
from utils.extras import safeformat

__version__ = 0.1


class SqlAlchemy(BaseDB):
    implementation = None
    def __init__(self, database, dialect=None, implementation=None, version=__version__, *args, **kwargs):
        super().__init__(version=version, *args, **kwargs)
        self.database = database
        if dialect:
            self.dialect = dialect
        else:
            self.dialect = self.__class__.__name__.lower()
        if implementation:
            self.implementation = implementation
        self.engine = None
        self.metadata = None
        self.session = None

    def __implementation(self):
        impl = "{dialect}://"
        if self.implementation:
            impl += self.implementation
        if self.database:
            impl += "/{database}"
        return safeformat(impl, **self.__dict__)

    def connect(self, encoding="utf-8", logging=True):
        self.log.debug("Initializing %s DB engine...", self.name)
        engine_impl = self.__implementation()
        self.log.debug("Engine implementation is %s", engine_impl)
        self.engine = create_engine(engine_impl, encoding=encoding, echo=logging)

        if logging:
            self.__own_logger()

        if not database_exists(self.engine.url):
            self.log.warn("Database '%s' not found. Creating it now!", self.database)
            create_database(self.engine.url)

        self.log.debug("Initializing %s DB session...", self.name)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        if self.session:
            self.log.info("Sucessfully initialized the %s DB session.", self.name)
        else:
            self.log.error("Failed initializing the %s DB session.", self.name)

    def close(self):
        self.log.info("Closing DB session...")
        if self.session:
            self.session.close()

    def create_schema(self, base):
        return base.metadata.create_all(self.engine)

    def __own_logger(self):
        import logging
        for logger_name in ["sqlalchemy.engine.base.Engine"]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(self.log.level)
            for handler in logger.handlers:
                logger.removeHandler(handler)
            for handler in self.log.handlers:
                logger.addHandler(handler)

    def commit_changes(self):
        self.log.info("Commiting all pending changes...")
        try:
            self.session.commit()
        except Exception as e:
            self.log.error("Fatal error occured. Rolling back to ensure DB consistency. \n %s", e)
            self.session.rollback()
            raise e

    def rollback_changes(self):
        self.log.info("Rolling back all pending changes...")
        self.session.rollback()

    def verify_object(self, obj):
        return issubclass(obj.__class__, object)

    def _add_object(self, obj):
        self.session.add(obj)

    def _remove_object(self, obj):
        self.session.delete(obj)

    def select(self, *args):
        query = select(*args)
        return self.session.execute(query)

    def select_object(self, obj):
        return self.session.query(obj)
