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
        self.log.debug("User '{.username}' (id={}) exists already.".format(user, int(stdout)))
        return True

    def add_user(self, user):
        if not self.user_exists(user):
            return self.backend.run(UserAdd.from_user(user), sudo=True)
        self.log.warn("Won't add user '{.username}' because it already exists.".format(user))
  
    def remove_user(self, user):
        if self.user_exists(user):
            return self.backend.run(UserDel.from_user(user), sudo=True)
        self.log.warn("Cannot remove inexistent user '{.username}'.".format(user))
    
    def modify_user(self, user):
        if self.user_exists(user):
            return self.backend.run(UserMod.from_user(user), sudo=True)
        self.log.warn("Cannot modify inexistent user '{.username}'.".format(user))

    def group_exists(self, group):
        exit_code, stdout, _ = self.backend.run(GroupCheck.from_group(group), sudo=True)
        if exit_code:
            return False
        self.log.debug("Group '{.name}' exists already.".format(group))
        return True

    def add_group(self, group):
        if not self.group_exists(group):
            return self.backend.run(GroupAdd.from_group(group), sudo=True)
        self.log.warn("Won't add group '{.name}' because it already exists.".format(group))

    def remove_group(self, group):
        if self.group_exists(group):
            return self.backend.run(GroupDel.from_group(group), sudo=True)
        self.log.warn("Cannot remove inexistent group '{.name}'.".format(group))

    def handle_user(self, user):
        if user.state.name == 'present':
            self.add_user(user)
        elif user.state.name == 'absent':
            self.remove_user(user)
        else:
            self.modify_user(user)
    
    def handle_group(self, group):
        if group.state.name == 'present':
            self.add_group(group)
        elif group.state.name == 'absent':
            self.remove_group(group)
