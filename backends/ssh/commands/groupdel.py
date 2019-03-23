from backends.command import BaseCommand
from objects.group import Group

__supported_os__ = ["Linux"]


class GroupDel(BaseCommand):
    def __init__(self, name):
        self.groupname = name
        super().__init__(__supported_os__)

    @staticmethod
    def from_group(group: Group):
        return GroupDel(name=group.name)

    def get_error_messages(self):
        return {
            0: "Success",
            2: "Invalid command syntax",
            6: "Specified group doesn't exist",
            8: "Can't remove user's primary group",
            10: "Can't update group file. Are you root?"
        }

    def get_template(self):
        # https://linux.die.net/man/8/groupdel
        cmd = "groupdel {group}"
        return cmd.format(group=self.groupname)
