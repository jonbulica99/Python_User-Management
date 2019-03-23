from backends.command import BaseCommand
from objects.group import Group

__supported_os__ = ["Linux"]


class GroupCheck(BaseCommand):
    def __init__(self, name):
        self.groupname = name
        super().__init__(__supported_os__)

    @staticmethod
    def from_group(group: Group):
        return GroupCheck(name=group.name)

    def get_error_messages(self):
        return {
            0: "Success"
        }

    def get_template(self):
        # If this command returns something, that means the group exists
        cmd = "getent group {name}"
        return cmd.format(name=self.groupname)
