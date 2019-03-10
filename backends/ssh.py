from backends.base import BaseBackend, MethodBackend

import paramiko

__version__ = 0.1


class SshBackend(BaseBackend):
    look_for_keys = True
    
    class Unix(MethodBackend):
        pass

    class Windows(MethodBackend):
        pass


    def __init__(self, host: host.Host, user: user.User, *args, **kwargs):
        super().__init__(version=__version__, *args, **kwargs)
        self.host = host
        self.user = user
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.shell = None
        
    def connect(self):
        super().connect()
        address, user, pwd = self.host.address, self.user.username, self.user.password
        self.client.connect(address, username=user, password=pwd, look_for_keys=self.look_for_keys)
        self.shell = self.client.invoke_shell()

    def __run(self, command):
        if self.shell:
            self.log.debug("Executing in the shell: '%s'", command)
            return self.shell.send(command + "\n")
        self.log.error("Shell was not initialized, you need to connect first.")

    def close(self):
        super().close()
        if(self.client != None):
            self.client.close()

    def sync_user(self, user):
        super().sync_user(user)
        # TODO continue here
        