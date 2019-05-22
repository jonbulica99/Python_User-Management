from backends.ssh.commands.useradd import UserAdd


class UserMod(UserAdd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_template(self):
        # https://linux.die.net/man/8/usermod
        return super().get_template().replace('useradd', 'usermod')
