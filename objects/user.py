from objects.base import *

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    stateID = Column(ForeignKey('state.id'), nullable=False, index=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(45), nullable=False)
    publicKey = Column(String(255))

    state = relationship('State')
    groups = relationship('Group', secondary="group_has_users")

    def __init__(self, state, firstname, lastname, password, publicKey=None, username=None):
        self.state = state
        self.stateID = state.id
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.publicKey = publicKey
        self.username = self.get_username(username)

    def get_username(self, username):
        if username:
            return username
        return (self.firstname + self.lastname).lower()

    def __repr__(self):
        return "User({})".format(self.username)
