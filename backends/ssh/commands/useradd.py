from backends.command import BaseCommand
from objects.user import User

import crypt

__supported_os__ = ["Linux"]


class UserAdd(BaseCommand):
    def __init__(self, first_name, last_name, password, username=None, groups=None, active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        if not username:
            username = first_name.lower() + last_name.lower()
        self.username = username
        self.groups = groups
        self.active = active
        self.salt = crypt.mksalt(crypt.METHOD_SHA512)
        super().__init__(__supported_os__)

    @staticmethod
    def from_user(user: User):
        return UserAdd(first_name=user.firstname, last_name=user.lastname, password=user.password,
            username=user.username, groups=user.groups, active=(user.state.name == 'active'))

    def get_error_messages(self):
        return {
            0: "Success",
            1: "Can't update password file. Are you root?",
            2: "Invalid command syntax. Are you a noob?",
            3: "Invalid argument to option",
            4: "UID already in use",
            6: "One or more of the specified groups ['{}'] don't exist".format(self.groups),
            9: "Username '{}' already in use".format(self.username),
            10: "Can't update group file. Are you root?",
            12: "Can't create home directory. Are you root?",
            13: "Can't create mail spool. Are you root?",
            14: "Can't update SELinux user mapping. Are you root?"
        }

    def get_template(self):
        # https://linux.die.net/man/8/useradd
        cmd, args, opts = "useradd {options} {username}", {}, []

        # set full name
        args["--comment"] = "{} {}".format(self.first_name, self.last_name)

        # check if we should disable user
        if not self.active:
            args["--shell"] = "/bin/nologin"

        # set password
        args["--password"] = self.get_encrypted_password(self.password)

        # set groups; if none are provided, we let the system decide
        if self.groups:
            args["--groups"] = ','.join([self.groups])

        return cmd.format(options=self.parse_opts(args), username=self.username)

    def get_encrypted_password(self, password):
        return crypt.crypt(password, self.salt)