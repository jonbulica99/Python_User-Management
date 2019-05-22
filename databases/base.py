from enum import Enum
from base import BaseObject
from utils.decorators import notimplemented


class BaseDB(BaseObject):
    __version__ = 0.2

    def __init__(self, name=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.log.debug("Initialized %s DB v%s", name, self.__version__)
        self.db = None

    def describe(self):
        return self.name

    @notimplemented
    def connect(self):
        pass
    
    @notimplemented
    def close(self):
        pass

    @notimplemented
    def verify_object(self, obj):
        pass

    @notimplemented
    def _add_object(self, obj):
        pass

    @notimplemented
    def _remove_object(self, obj):
        pass

    @notimplemented
    def select(self, *args):
        pass

    def add_object(self, obj):
        if self.verify_object(obj):
            self.log.debug("Inserting %s", obj)
            self._add_object(obj)
        else:
            self.log.error("Cannot insert invalid object: %s", obj)

    def add_objects(self, obj_list):
        for obj in obj_list:
            self.add_object(obj)

    def remove_object(self, obj):
        if self.verify_object(obj):
            self.log.debug("Removing %s", obj)
            self._remove_object(obj)
        else:
            self.log.error("Cannot remove invalid object: %s", obj)
    
    def remove_objects(self, obj_list):
        for obj in obj_list:
            self.remove_object(obj)

    @notimplemented
    def commit_changes(self):
        pass

    @notimplemented
    def rollback_changes(self):
        pass
