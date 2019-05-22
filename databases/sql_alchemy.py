from objects import db
from databases.base import BaseDB
from sqlalchemy_utils import database_exists, create_database
from utils.extras import safeformat

__version__ = 0.1


class SqlAlchemy(BaseDB):
    def __init__(self, database, dialect=None, implementation=None, logging=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database
        if dialect:
            self.dialect = dialect
        else:
            self.dialect = self.__class__.__name__.lower()
        if implementation:
            self.implementation = implementation
        self.logging = logging

    def __own_logger(self):
        import logging
        for logger_name in ["sqlalchemy.engine.base.Engine"]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(self.log.level)
            for handler in logger.handlers:
                logger.removeHandler(handler)
            for handler in self.log.handlers:
                logger.addHandler(handler)

    def _connect(self):
        self.log.debug("Initializing %s DB engine...", self.name)
        # setup logging
        if self.logging:
            self.__own_logger()

        # engine implementation
        impl = "{dialect}://"
        if self.implementation:
            impl += self.implementation
        if self.database:
            impl += "/{database}"
        engine_impl = safeformat(impl, **self.__dict__)
        self.log.debug("Engine implementation is %s", engine_impl)
        return engine_impl

    def connect(self, flask_app):
        impl = self._connect()
        self.log.debug("Checking if database exists")
        try:
            if not database_exists(impl):
                self.log.warn("Database '%s' not found. Creating it now!", self.database)
                create_database(impl)
            self.log.info("Attempting flask integration...")
            flask_app.config['SQLALCHEMY_DATABASE_URI'] = impl
            flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            db.init_app(flask_app)
            return db
        except Exception as e:
            self.log.error("Connection failed: %s", e)
            raise e

    def close(self):
        self.log.info("Closing DB session...")
        if db.session:
            db.session.remove()

    def create_schema(self):
        self.log.info("Creating database schema...")
        return db.create_all()

    def commit_changes(self):
        self.log.info("Commiting all pending changes...")
        db.session.commit()

    def rollback_changes(self):
        self.log.info("Rolling back all pending changes...")
        db.session.rollback()

    def verify_object(self, obj):
        return issubclass(obj.__class__, object)

    def _add_object(self, obj):
        db.session.add(obj)

    def _remove_object(self, obj):
        db.session.delete(obj)

    def select(self, *args):
        pass

    def select_object(self, obj):
        pass
