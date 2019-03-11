import unittest

from utils.decorators import expect
from backends.ssh.main import SshBackend

# from backends.ssh.commands import *


class SshBackendTests(unittest.TestCase):
    pass


class SshCommandTests(unittest.TestCase):

    @expect(ModuleNotFoundError, "Only UNIX systems support crypt!")
    def test_useradd(self):
        from backends.ssh.commands.useradd import UserAdd
        user = UserAdd(first_name="Max", last_name="Mustermann",
                      password="hunter2")
        cmd = user.get()
        self.assertEqual(
            cmd, "useradd '--comment' 'Max Mustermann' '--password' '{}' maxmustermann".format(user.get_encrypted_password("hunter2")))

    def test_userdel(self):
        from backends.ssh.commands.userdel import UserDel
        user = UserDel("maxmustermann", force=True, remove_home=True)
        cmd = user.get()
        self.assertEqual(cmd, "userdel '--force' '--remove' maxmustermann")


if __name__ == '__main__':
    unittest.main()
