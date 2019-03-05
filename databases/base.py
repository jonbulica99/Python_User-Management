from enum import Enum
from utils.log import Logger

__version__ = 0.2


class BaseDB:
    def __init__(self, name=None, version=__version__, *args, **kwargs):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.version = version
        self.log = Logger(name).get()
        self.log.debug("Initialized %s DB v%s", name, version)
        self.db = None

    def describe(self):
        return self.name

    def connect(self):
        raise NotImplementedError("You should override this method in the child implementation!")
    
    def close(self):
        raise NotImplementedError("You should override this method in the child implementation!")

    def verify_object(self, obj):
        raise NotImplementedError("You should override this method in the child implementation!")

    def _add_object(self, obj):
        raise NotImplementedError("You should override this method in the child implementation!")

    def _remove_object(self, obj):
        raise NotImplementedError("You should override this method in the child implementation!")

    def select(self, *args):
        raise NotImplementedError("You should override this method in the child implementation!")

    def add_object(self, obj):
        if self.verify_object(obj):
            self.log.debug("Inserting %s", obj)
            self._add_object(obj)
        else:
            self.log.error("Cannot insert invalid object: %s", obj)

    def add_objects(self, list):
        for obj in list:
            self.add_object(obj)

    def remove_object(self, obj):
        if self.verify_object(obj):
            self.log.debug("Removing %s", obj)
            self._remove_object(obj)
        else:
            self.log.error("Cannot remove invalid object: %s", obj)
    
    def remove_objects(self, list):
        for obj in list:
            self.remove_object(obj)

    def commit_changes(self):
        raise NotImplementedError("You should override this method in the child implementation!")

    def rollback_changes(self):
        raise NotImplementedError("You should override this method in the child implementation!")
