from objects.base import *


class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), unique=True, nullable=False)
    address = Column(String(45), unique=True, nullable=False)
    port = Column(Integer)
    userID = Column(ForeignKey('users.id'), nullable=False, index=True)

    user = relationship('User')

    def __init__(self, name, address, user, port=22):
        self.name = name
        self.address = address
        self.port = port
        self.userID = user.id

    def __repr__(self):
        return "Host({}, {})".format(self.name, self.address)
