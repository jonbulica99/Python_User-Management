from objects.base import BaseObject

__version__ = 0.1
__db_name__ = "groups"


class Group(BaseObject):
    def __init__(self):
        super().__init__(version=__version__, db_name=__db_name__)
