from objects.base import *


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    parentID = Column(ForeignKey('groups.id'), index=True)
    stateID = Column(ForeignKey('state.id'), nullable=False, index=True)
    name = Column(String(45), unique=True, nullable=False)

    parent = relationship('Group', remote_side=[id])
    state = relationship('State')
    users = relationship('User', secondary="group_has_users")

    def __init__(self, state, name, parent=None):
        if parent:
            self.parentID = parent.id
        self.stateID = state.id
        self.name = name

    def __repr__(self):
        return "Group({})".format(self.name)

    def as_dict(self, joins=True):
        out = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joins:
            out.update({
                "joins": {
                    "state": self.state.name,
                    "users": [{"id": user.id, "username": user.username} for user in self.users],
                    "parent": self.parent.name if self.parent else None
                }
            })
        return out
