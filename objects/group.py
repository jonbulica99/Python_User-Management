from objects.base import db, BaseObject


class Group(db.Model, BaseObject):
    id = db.Column(db.Integer, primary_key=True)
    parentID = db.Column(db.ForeignKey('group.id'), index=True)
    stateID = db.Column(db.ForeignKey('state.id'), nullable=False, index=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    parent = db.relationship('Group', remote_side=[id])
    state = db.relationship('State')
    users = db.relationship('User', secondary="group_has_users")

    def __init__(self, state, name, parent=None, *args, **kwargs):
        if parent:
            self.parentID = parent.id
        self.state = state
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
                    "parent": {
                        'id': self.parent.id,
                        'name': self.parent.name
                    } if self.parent else None
                }
            })
        return out
