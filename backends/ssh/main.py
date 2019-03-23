from backends.backend import BaseBackend
from backends.command import BaseCommand
from fabric import Connection, Config
from enum import Enum

import os

__version__ = 0.1


class SshBackend(BaseBackend):
    # http://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html
    #init_cmd = 'source ~/.bashrc && echo $PATH'
    init_cmd = 'echo $PATH'

    look_for_keys = True

    def __init__(self, host, user=None, *args, **kwargs):
        super().__init__(version=__version__, *args, **kwargs)
        self.host = host
        if not user:
            user = host.user
        self.user = user
        self.config = Config(
            # sudo is handled by fabric itself
            overrides={
                'sudo': {'password': user.password}
            })

    def __del__(self):
        if self.connection:
            self.connection.close()

    def connect(self):
        super().connect()
        self.connection = Connection(self.host.address,
                                     user=self.user.username,
                                     port=self.host.port or 22,
                                     connect_kwargs={
                                        'password': self.user.password,
                                        'look_for_keys': self.look_for_keys
                                     },
                                     config=self.config)

        try:
            self.connection.open()
        except Exception as e:
            self.log.error('SSH connection failure: %s', e)

        if self.connection.is_connected:
            self.log.debug('Successfully established ssh connection: %s@%s',
                           self.user.username, self.host.address)

            # source the user profile
            self.__run(self.init_cmd)
            self.log.debug('SSH session setup successful')

    def run(self, command, sudo=False):
        if not issubclass(command.__class__, BaseCommand):
            self.log.error(
                "Only children of BaseCommand can be ran through this method!")
            raise AssertionError
        exit_code, stdout, stderr = self.__run(command.get(), sudo)
        error_msg = command.get_error_message(exit_code)

        if stdout:
            self.log.debug("stdout => %s", stdout)
        if stderr:
            self.log.debug("stderr => %s", stderr)
        if exit_code:
            self.log.error("Error [%s]: %s", exit_code, error_msg)
        return exit_code, stdout, stderr

    def __run(self, cmd, sudo=False):
        if self.connection:
            for command in cmd.split('&&'):
                # remove trailing and leading whitespace
                command = command.strip()
                self.log.info("Executing: '%s'", command)
                if sudo:
                    out = self.connection.sudo(command, warn=True)
                else:
                    out = self.connection.run(command, warn=True)
                if out.return_code:
                    break # If there are any errors, stop the execution
            return out.return_code, out.stdout, out.stderr

    def close(self):
        super().close()
        if self.connection:
            self.connection.close()
