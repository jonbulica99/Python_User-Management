from objects.base import BaseObject

__version__ = 0.1


class Host(BaseObject):
    def __init__(self, version=__version__):
        super().__init__()
