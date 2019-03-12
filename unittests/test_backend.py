import unittest

from utils.decorators import expect
from backends.ssh.main import SshBackend
from objects import *

# from backends.ssh.commands import *


class SshBackendTests(unittest.TestCase):
    pass


class SshCommandTests(unittest.TestCase):
    def test_useradd(self):
        from backends.ssh.commands.useradd import UserAdd
        user = UserAdd(first_name="Max", last_name="Mustermann",
                       password="hunter2")
        cmd = user.get()
        self.assertEqual(
            cmd, "useradd '--comment' 'Max Mustermann' '--shell' '/bin/bash' '--password' '{}' maxmustermann".format(user.get_encrypted_password("hunter2")))

    def test_useradd2(self):
        max_muster = User(State('present'), 'Max', 'Mustermann', 'supersecure', None, groups=['root', 'www-data'])
        
        from backends.ssh.commands.useradd import UserAdd
        user = UserAdd.from_user(max_muster)
        cmd = user.get()
        self.assertEqual(
            cmd, "useradd '--comment' 'Max Mustermann' '--shell' '/bin/bash' '--password' '{}' '--groups' 'root,www-data' maxmustermann".format(user.get_encrypted_password("supersecure")))

    def test_usermod(self):
        from backends.ssh.commands.usermod import UserMod
        user = UserMod(first_name="Max", last_name="Mustermann",
                       password="hunter2")
        cmd = user.get()
        self.assertEqual(
            cmd, "usermod '--comment' 'Max Mustermann' '--shell' '/bin/bash' '--password' '{}' maxmustermann".format(user.get_encrypted_password("hunter2")))

    def test_userdel(self):
        from backends.ssh.commands.userdel import UserDel
        user = UserDel("maxmustermann", force=True, remove_home=True)
        cmd = user.get()
        self.assertEqual(cmd, "userdel '--force' '--remove' maxmustermann")


if __name__ == '__main__':
    unittest.main()
