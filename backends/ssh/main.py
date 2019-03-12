from backends.backend import BaseBackend
from backends.command import BaseCommand
from enum import Enum

import paramiko

__version__ = 0.1

class SshBackend(BaseBackend):
    class BecomeMethod(Enum):
        SU = 'su'
        SUDO = 'sudo'
    
    look_for_keys = True

    def __init__(self, host, user, *args, **kwargs):
        super().__init__(version=__version__, *args, **kwargs)
        self.host = host
        self.user = user
        self.client = None
        
    def connect(self):
        super().connect()
        address, user, pwd = self.host.address, self.user.username, self.user.password
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=user, password=pwd, look_for_keys=self.look_for_keys)
        # TODO https://stackoverflow.com/questions/35821184/implement-an-interactive-shell-over-ssh-in-python-using-paramiko
        self.shell = self.client.invoke_shell()

    def become(self, method, password, user="root"):
        self.log.info("Trying to become root...")
        method = self.BecomeMethod(method)
        cmd = method.value
        if cmd == 'su':
            cmd += ' %s' % user
        elif cmd == 'sudo':
            cmd += ' su'
        stdin, stdout, stderr = self.__run(cmd)
        stdin.write('%s\n' % password)
        stdin.flush()

    def run(self, command):
        if not issubclass(command.__class__, BaseCommand):
            self.log.error("Only children of BaseCommand can be ran through this method!")
            raise AssertionError
        stdin, stdout, ssh_stderr = self.__run(command.get())
        out = stdout.read().decode()
        stdin.flush()
        exit_code = stdout.channel.recv_exit_status()
        error_msg = command.get_error_message(exit_code)
        if exit_code:
            self.log.error("Error [%s]: %s", exit_code, error_msg)
        else:
            self.log.debug('Received answer from host: %s', out)
        return out

    def __run(self, cmd):
        if self.shell:
            self.log.info("Executing in the shell: '%s'", cmd)
            return self.shell.exec_command(cmd + '\n')
        self.log.error("The remote shell was not initialized, you need to connect first.")

    def close(self):
        super().close()
        if(self.client != None):
            self.client.close()
