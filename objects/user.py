from objects.base import db, BaseObject


class User(db.Model, BaseObject):
    id = db.Column(db.Integer, primary_key=True)
    stateID = db.Column(db.ForeignKey('state.id'), nullable=False, index=True)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    publicKey = db.Column(db.String(255))

    state = db.relationship('State')
    groups = db.relationship('Group', secondary="group_has_users")

    def __init__(self, state, username=None, *args, **kwargs):
        self.state = state
        self.stateID = state.id
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.password = kwargs.get('password')
        self.publicKey = kwargs.get('publicKey', None)
        self.username = self.get_username(username)

    def get_username(self, username):
        if username:
            return username
        return (self.firstname + self.lastname).lower()

    def __repr__(self):
        return "User({})".format(self.username)

    def as_dict(self, joins=True):
        out = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joins:
            out.update({
                "joins": {
                    "state": self.state.name,
                    "groups": [{'id': group.id, 'name': group.name} for group in self.groups]
                }
            })
        return out
