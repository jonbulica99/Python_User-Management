from backends.ssh.commands.useradd import UserAdd

__supported_os__ = ["Linux"]


class UserMod(UserAdd):
    def __init__(self, first_name, last_name, password, username=None, groups=None, active=True):
        super().__init__(first_name, last_name, password, username, groups, active)

    def get_template(self):
        # https://linux.die.net/man/8/usermod
        return super().get_template().replace('useradd', 'usermod')
