from objects.base import *

group_has_users = Table(
    'group_has_users', Base.metadata,
    Column('group_id', ForeignKey('groups.id'), primary_key=True, nullable=False, index=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True, nullable=False, index=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    stateID = Column(ForeignKey('state.id'), nullable=False, index=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    username = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    publicKey = Column(String(255))

    state = relationship('State')
    groups = relationship('Group', secondary="group_has_users")

    def __init__(self, stateID, firstname, lastname, password, publicKey, username=None):
        self.stateID = stateID
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.publicKey = publicKey
        self.username = self.get_username(username)

    def get_username(self, username):
        if username:
            return username
        return self.firstname[:1] + self.lastname
