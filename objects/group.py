from objects.base import *


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    parentID = Column(ForeignKey('groups.id'), index=True)
    stateID = Column(ForeignKey('state.id'), nullable=False, index=True)
    name = Column(String(45), nullable=False)

    parent = relationship('Group', remote_side=[id])
    state = relationship('State')
    users = relationship('User', secondary="group_has_users")

    def __init__(self, parentID, stateID, name):
        self.parentID = parentID
        self.stateID = stateID
        self.name = name
