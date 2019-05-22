from backends.command import BaseCommand
from objects.user import User


class AddSshKey(BaseCommand):
    def __init__(self, username, key, append=True):
        self.username = username
        self.key = key
        self.append = append
        super().__init__()

    @staticmethod
    def from_user(user: User):
        return AddSshKey(username=user.username, key=user.publicKey)

    def get_error_messages(self):
        return {
            0: "Success"
        }

    def get_template(self):
        # do not assume homedir is /home/$username
        user_home = "$( getent passwd '{}' | cut -d: -f6 )".format(self.username)
        ssh_dir = "{}/.ssh".format(user_home)
        authorized_keys = "{}/authorized_keys".format(ssh_dir)

        append = 'oflag=append' if self.append else ''
        commands = [
            "mkdir -p {ssh}",
            "touch {authorized_keys}",
            "echo '{key}' | sudo dd conv=notrunc of={authorized_keys} {append}",
            # authorized_keys file must be private, otherwise the ssh server WILL ignore it
            "chown -R {username}:{username} {ssh}",
            "chmod 0600 {authorized_keys}"
        ]
        return ' && '.join(commands).format(username=self.username, ssh=ssh_dir, authorized_keys=authorized_keys, key=self.key, append=append)
