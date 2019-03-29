from objects.base import db, BaseObject


class State(db.Model, BaseObject):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "State({})".format(self.name)
