from backends.command import BaseCommand
from objects.user import User


class UserCheck(BaseCommand):
    def __init__(self, username):
        self.username = username
        super().__init__()

    @staticmethod
    def from_user(user: User):
        return UserCheck(username=user.username)

    def get_error_messages(self):
        return {
            0: "Success"
        }

    def get_template(self):
        # If this command returns an id, that means the user exists
        cmd = "id -u {username}"
        return cmd.format(username=self.username)
