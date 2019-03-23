from objects.base import *
from objects import User, Group


class UserGroupLink(Base):
    __tablename__ = 'group_has_users'

    userid = Column('user_id', ForeignKey('users.id'), primary_key=True, nullable=False, index=True)
    groupid = Column('group_id', ForeignKey('groups.id'), primary_key=True, nullable=False, index=True)
    user = relationship(User, backref=backref("users_assoc"))
    group = relationship(Group, backref=backref("groups_assoc"))

    def __init__(self, user, group):
        self.userid = user.id
        self.groupid = group.id

    def __repr__(self):
        return "UserGroupLink({} <=> {})".format(self.user, self.group)
