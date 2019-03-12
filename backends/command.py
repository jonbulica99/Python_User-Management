from utils.log import Logger
from utils.decorators import notimplemented, expect
from utils.extras import safeformat
from enum import Enum

import platform


class BaseCommand:
    class Os(Enum):
        Linux = "Linux"
        Windows = "Windows"
        OSX = "Darwin"

    class OsNotSupportedException(Exception):
        def __init__(self, message):
            self.message = message

    def __init__(self, supported_os):
        self.name = name = self.__class__.__name__
        self.log = Logger(name).get()
        self.log.debug("Initialized %s command", name)
        self.supported_os = self.parse_supported_os(supported_os)
        self.error_messages = []
        self.cmd = self.__generate()

    # @expect()
    def parse_supported_os(self, os):
        self.log.debug("Parsing supported operating systems.")
        if not isinstance(os, list):
            os = [os]
        return [self.Os(i) for i in os]

    def __generate(self):
        user_os = platform.system()
        if self.Os(user_os) not in self.supported_os:
            raise self.OsNotSupportedException("{} is not supported by your OS.".format(self.name))
        cmd = self.get_template()
        self.log.debug("Generated command '%s'", cmd)
        return cmd

    def get(self):
        return self.cmd

    @notimplemented
    def get_template(self):
        pass

    @notimplemented
    def get_error_messages(self):
        pass

    @expect(IndexError, "An error occured!")
    def get_error_message(self, exit_code):
        return list(self.get_error_messages().values())[exit_code]
        
    @staticmethod
    def parse_opts(opts):
        ret = []
        for key, value in opts.items():
            ret.append(key)
            if value:
                ret.append(value)
        return ' '.join("'{}'".format(i) for i in ret)


    add_user = None
    del_user = None
    en_user = None
    dis_user = None
    add_user_group = None
    del_user_group = None
    add_group = None
    del_group = None
