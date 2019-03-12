import unittest

from backends.ssh.main import SshBackend
from backends.ssh.commands import *
from objects import *

# from backends.ssh.commands import *


class SshBackendTests(unittest.TestCase):
    pass


class SshCommandTests(unittest.TestCase):
    def test_useradd(self):
        user = UserAdd(first_name="Max", last_name="Mustermann",
                       password="hunter2")
        cmd = user.get()
        self.assertEqual(
            cmd, "useradd '--comment' 'Max Mustermann' '--shell' '/bin/bash' '--password' '{}' maxmustermann".format(user.get_encrypted_password("hunter2")))

    def test_useradd2(self):
        max_muster = User(State('present'), 'Max', 'Mustermann',
                          'supersecure', None, groups=['root', 'www-data'])
        user = UserAdd.from_user(max_muster)
        cmd = user.get()
        self.assertEqual(
            cmd, "useradd '--comment' 'Max Mustermann' '--shell' '/bin/bash' '--password' '{}' '--groups' 'root,www-data' maxmustermann".format(user.get_encrypted_password("supersecure")))

    def test_usermod(self):
        user = UserMod(first_name="Max", last_name="Mustermann",
                       password="hunter2")
        cmd = user.get()
        self.assertEqual(
            cmd, "usermod '--comment' 'Max Mustermann' '--shell' '/bin/bash' '--password' '{}' maxmustermann".format(user.get_encrypted_password("hunter2")))

    def test_userdel(self):
        user = UserDel("maxmustermann", force=True, remove_home=True)
        cmd = user.get()
        self.assertEqual(cmd, "userdel '--force' '--remove' maxmustermann")


if __name__ == '__main__':
    unittest.main()
