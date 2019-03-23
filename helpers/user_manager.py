from utils.log import Logger
from backends.ssh.commands import *

class UserManager:
    def __init__(self, backend):
        self.log = Logger(self.__class__.__name__).get()
        self.backend = backend

    def user_exists(self, user):
        exit_code, stdout, _ = self.backend.run(UserCheck.from_user(user), sudo=True)
        if exit_code:
            return False
        
        self.log.warn("User '{.username}' (id={}) exists already.".format(user, int(stdout)))
        return True

    def add_user(self, user):
        if not self.user_exists(user):
            return self.backend.run(UserAdd.from_user(user), sudo=True)
  
    def remove_user(self, user):
        return self.backend.run(UserDel.from_user(user), sudo=True)
