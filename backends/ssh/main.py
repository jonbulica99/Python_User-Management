from backends.backend import BaseBackend
from backends.command import BaseCommand
from enum import Enum

import re
import os
import paramiko

__version__ = 0.1


class SshBackend(BaseBackend):
    class BecomeMethod(Enum):
        SU = 'su'
        SUDO = 'sudo'

    # http://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html
    #init_cmd = 'source ~/.bashrc && echo $PATH'
    init_cmd = 'echo $PATH'

    look_for_keys = True
    bufsize = 4096

    def __init__(self, host, user, become=None, *args, **kwargs):
        super().__init__(version=__version__, *args, **kwargs)
        self.host = host
        self.user = user
        if not become:
            # use sudo/su if user is not root
            become = self.user.username != 'root'
        self.become = become
        self.client = self.session = None

    def __del__(self):
        if self.client:
            self.client.close()

    def connect(self):
        super().connect()
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.client.AutoAddPolicy())

        try:
            self.client.connect(
                self.host.address,
                username=self.user.username,
                password=self.user.password,
                port=self.host.port or 22,
                look_for_keys=self.look_for_keys
            )
        except paramiko.ssh_exception.BadHostKeyException as e:
            self.log.error('Host key mismatch for %s', self.host.address)
        except paramiko.ssh_exception.AuthenticationException as e:
            self.log.error('Invalid username/password: %s', e)
        except Exception as e:
            self.log.error('SSH connection failure: %s', e)
        
        if self.client.get_transport():
            self.log.debug('Successfully established ssh connection: %s@%s', self.user.username, self.host.address)
        
        try:
            self.session = s = self.client.invoke_shell()
            self.stdin = s.makefile('wb')
        except Exception as e:
            self.log.error('SSH session failure: %s', e)

        if self.session:
            # source the user profile
            self.__run(self.init_cmd)
            self.log.debug('SSH session setup successful')


    def become_user(self, method, password, user="root"):
        self.log.info("Trying to become root...")
        method = self.BecomeMethod(method)
        cmd = method.value
        if cmd == 'su':
            cmd += ' %s' % user
        elif cmd == 'sudo':
            cmd += ' su'
        _, stdin, stdout, stderr = self.__run(cmd)
        stdin.write('%s\n' % password)
        stdin.flush()

    def run(self, command):
        if not issubclass(command.__class__, BaseCommand):
            self.log.error("Only children of BaseCommand can be ran through this method!")
            raise AssertionError
        exit_code, _, stdout, stderr = self.__run(command.get())
        error_msg = command.get_error_message(exit_code)

        self.log.debug("stdout => %s", stdout)
        if stderr:
            self.log.debug("stderr => %s", stderr)
        if exit_code:
            self.log.error("Error [%s]: %s", exit_code, error_msg)
        return stdout


    def __run(self, cmd):
        if self.session:
            stdout = self.session.makefile('rb')
            self.log.info("Executing: '%s'", cmd)
            if not cmd.endswith('\n'):
                cmd += '\n'
            try:
                self.stdin.write(cmd)
                finish = 'finished with exit status'
                echo_cmd = 'echo {} $?'.format(finish)
                self.stdin.write(echo_cmd + '\n')
                shin = self.stdin
                self.stdin.flush()

                print(stdout.read())
                exit_code = 0
                return exit_code, shin, stdout, stderr
            except IOError as e:
                self.log.error("Failed to execute command: %s", e)
        self.log.error("No SSH session initialized, you need to connect first.")

    def close(self):
        super().close()
        if self.client:
            self.client.close()
