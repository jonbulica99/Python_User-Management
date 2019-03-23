from backends.command import BaseCommand
from objects.group import Group

__supported_os__ = ["Linux"]


class GroupAdd(BaseCommand):
    def __init__(self, name, system_group=False):
        self.groupname = name
        self.system_group = system_group
        super().__init__(__supported_os__)

    @staticmethod
    def from_group(group: Group):
        return GroupAdd(name=group.name)

    def get_error_messages(self):
        return {
            0: "Success",
            2: "Invalid command syntax",
            3: "Invalid argument to option",
            4: "GID not unique (when -o not used)",
            9: "Group name not unique",
            10:" can't update group file"
        }

    def get_template(self):
        # https://linux.die.net/man/8/groupadd
        cmd, args, opts = "groupadd {options} {group}", {}, []

        # make the group a system group
        if self.system_group:
            args["--system"] = None

        return cmd.format(options=self.parse_opts(args), group=self.groupname)
