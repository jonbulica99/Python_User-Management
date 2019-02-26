import ZODB
import transaction
from enum import Enum
from utils.log import Logger
from objects.base import BaseObject

__version__ = 0.2


class BaseDB:
    class Action(Enum):
        ADD = 0
        DELETE = 1

    def __init__(self, name=None, version=__version__):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s v%s", name, version)
        self.db = None

    def describe(self):
        return self.name

    def connect(self):
        if self.db:
            try:
                self.connection = self.db.open()
                self.log.info("Established database connection to: %s", self.describe())
                self.cursor = self.connection.root()
                return self.cursor
            except Exception as e:
                self.log.error("Connection failure: %s", e)
        else:
            self.log.error("Failed to establish a valid database connection.")

    def commit(self):
        self.log.info("Commiting transaction into the database.")
        transaction.commit()

    def discard(self):
        pass

    def verify_object(self, obj: BaseObject):
        print(obj.__class__, obj.db_name)
        return issubclass(obj.__class__, BaseObject) and obj.db_name

    def _db_action_delegate(self, action: Action, obj: BaseObject):
        if self.verify_object(obj):
            if self.cursor:
                if not obj.db_name in self.cursor:
                    self.cursor[obj.db_name] = {}
                table = self.cursor[obj.db_name]
                if action == self.Action.ADD:
                    table.append(obj)
                elif action == self.Action.DELETE:
                    if obj in table:
                        table.remove(obj)
                    else:
                        self.log.error("%s does not exist in the table '%s'", obj.name, obj.db_name)
                        return False
                else:
                    raise NotImplementedError("This action was not implemented, valid actions are: {}".format(", ".join([n.name for n in self.Action])))
                
                self.cursor[obj.db_name] = table
                return True
            else:
                self.log.error("Could not add object to the database, because no cursor was found. Did you call connect()?")
        else:
            self.log.error("You can only add objects extending BaseObject to the database.")

    def add_object(self, obj):
        self.log.debug("Adding %s object", obj.name)
        if self._db_action_delegate(self.Action.ADD, obj):
            self.log.info("Added %s object", obj.name)

    def remove_object(self, obj):
        self.log.debug("Removing %s object", obj.name)
        if self._db_action_delegate(self.Action.DELETE, obj):
            self.log.info("Removed %s object", obj.name)
