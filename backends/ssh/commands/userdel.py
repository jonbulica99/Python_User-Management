from backends.command import BaseCommand
from objects.user import User

__supported_os__ = ["Linux"]


class UserDel(BaseCommand):
    def __init__(self, username, force=False, remove_home=True):
        self.username = username
        self.force = force
        self.remove_home = remove_home
        super().__init__(__supported_os__)

    @staticmethod
    def from_user(user: User):
        return UserDel(username=user.username)

    def get_error_messages(self):
        return {
            0: "Success",
            1: "Can't update password file. Are you root?",
            2: "Invalid command syntax. Are you a noob?",
            6: "Specified user doesn't exist",
            8: "User currently logged in",
            10: "Can't update group file. Are you root?",
            12: "Can't remove home directory"
        }

    def get_template(self):
        # https://linux.die.net/man/8/userdel
        cmd, args, opts = "userdel {options} {username}", {}, []

        # force remove user
        if self.force:
            args["--force"] = None

        if self.remove_home:
            args["--remove"] = None

        return cmd.format(options=self.parse_opts(args), username=self.username)
