from backends.ssh.commands.addsshkey import AddSshKey
from backends.command import BaseCommand
from objects.user import User
from utils.decorators import expect


class UserAdd(BaseCommand):
    @expect(ImportError, "Only UNIX systems support crypt!")
    def __init__(self, *args, **kwargs):
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.password = kwargs.get('password')
        self.username = kwargs.get(
            'username', (self.first_name + self.last_name).lower())
        self.groups = kwargs.get('groups', None)
        self.active = kwargs.get('active', True)
        self.pubkey = kwargs.get('pubkey', None)
        self.change_pwd_on_first_login = kwargs.get(
            'change_pwd_on_first_login', True)
        from helpers.crypt_helper import crypt
        self._crypt = crypt
        self.salt = crypt.mksalt(crypt.METHOD_SHA512)
        super().__init__()

    @staticmethod
    def from_user(user: User):
        return UserAdd(first_name=user.firstname, last_name=user.lastname, password=user.password,
                       username=user.username, groups=user.groups, active=(user.state.name == 'present'), pubkey=user.publicKey)

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

        # make sure to create home die
        args["--create-home"] = None

        # check if we should disable user
        if self.active:
            args["--shell"] = "/bin/bash"
        else:
            args["--shell"] = "/bin/nologin"

        # set password
        args["--password"] = self.get_encrypted_password(self.password)

        # set groups; if none are provided, we let the system decide
        if self.groups:
            grps = self.groups
            if not isinstance(self.groups, list):
                grps = [self.groups]
            args["--groups"] = ','.join(g.name for g in grps)

        out = cmd.format(options=self.parse_opts(args), username=self.username)

        if self.change_pwd_on_first_login:
            # https://unix.stackexchange.com/questions/173708/how-do-i-force-a-user-to-change-a-password-at-the-first-time-login-using-ssh
            out += " && chage -d 0 {username}".format(username=self.username)

        if self.pubkey:
            out += ' && %s' % AddSshKey(username=self.username,
                                        key=self.pubkey).get_template()
        return out

    def get_encrypted_password(self, password):
        return self._crypt.crypt(password, self.salt)
