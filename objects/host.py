from objects.base import db, BaseObject


class Host(db.Model, BaseObject):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    address = db.Column(db.String(45), unique=True, nullable=False)
    port = db.Column(db.Integer)
    userID = db.Column(db.ForeignKey('user.id'), nullable=False, index=True)

    user = db.relationship('User')

    def __init__(self, name, address, user, port=22):
        self.name = name
        self.address = address
        self.port = port
        self.userID = user.id

    def __repr__(self):
        return "Host({}, {})".format(self.name, self.address)

    def as_dict(self, joins=True):
        out = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joins:
            out.update({
                "joins": {
                    "user": self.user.as_dict()
                }
            })
        return out
