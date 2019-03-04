from objects.base import *


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)

    def __init__(self, name):
        self.name = name
