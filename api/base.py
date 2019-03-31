from objects import *
from enum import Enum
from flask_restful import Resource, reqparse
from databases.sql_alchemy import SqlAlchemy
from utils.log import Logger
from utils.decorators import notimplemented

__version__ = 0.1


class BaseEndpoint(Resource):
    class Method(Enum):
        Add = 0
        Edit = 1
        Delete = 2

    def __init__(self, name=None, version=__version__, *args, **kwargs):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s v%s", name, version)
        self.parser = reqparse.RequestParser()
        self.success_message = "Operation executed successfully."
        self.error_message = "Something went terribly wrong. Please consult your system administrator for further assistance."
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls, database):
        # we need the database class extending SqlAlchemy()
        if issubclass(database.__class__, SqlAlchemy):
            cls.db = database
        else:
            raise NotImplementedError(
                "Only database classes extending SqlAlchemy are allowed!")
        return cls

    def return_error(self, exception, data=None, message=None):
        self.log.error("Request resulted in error: %s", exception)
        return {
            "success": False,
            "message": message or self.error_message,
            "exception": str(exception),
            "data": data
        }

    def return_success(self, data=None, message=None):
        self.log.debug("Request was successful")
        return {
            "success": True,
            "message": message or self.success_message,
            "data": data
        }

    def safe_add(self, obj):
        self.log.info("Inserting %s into database", obj)
        try:
            self.db.add_object(obj)
        except Exception as e:
            return self.return_error(e)

    def safe_edit(self, local_obj, db_obj):
        self.log.info("Changing database object %s into %s", db_obj, local_obj)
        try:
            for column in local_obj.__table__.columns:
                if column.name != 'id':
                    setattr(db_obj, column.name,
                            local_obj.as_dict().get(column.name))
        except Exception as e:
            return self.return_error(e)

    def safe_delete(self, obj):
        self.log.info("Deleting %s from database", obj)
        try:
            self.db.remove_object(obj)
        except Exception as e:
            return self.return_error(e)

    def safe_commit(self, data):
        try:
            self.db.commit_changes()
        except Exception as e:
            return self.return_error(e, data=data)

        # if everything went ok inform the user
        return self.return_success(data=data)
