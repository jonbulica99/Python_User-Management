from objects.base import db, BaseObject
from objects import User, Group


class UserGroupLink(db.Model, BaseObject):
    __tablename__ = 'group_has_users'

    userid = db.Column('user_id', db.ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    groupid = db.Column('group_id', db.ForeignKey('group.id'), primary_key=True, nullable=False, index=True)
    user = db.relationship(User, backref=db.backref("users_assoc", cascade="all, delete-orphan", single_parent=True))
    group = db.relationship(Group, backref=db.backref("groups_assoc", cascade="all, delete-orphan", single_parent=True))

    def __init__(self, user, group):
        self.userid = user.id
        self.groupid = group.id

    def __repr__(self):
        return "UserGroupLink({} <=> {})".format(self.user, self.group)
