""" Description """

import os.path
import logging
from fabric.api import env, output, put, sudo

from config import *
from config import __file__ as config_file
import common


CMD_LOG, LOG_FILE = common.initiate_logger(CMD_LOG)
DEBUG_LOG = logging.getLogger(DEBUG_LOG)

# Fabric variables setup
env.password = SERVER_HOST_PASSWORD
env.host_string = '@'.join((SERVER_HOST_NAME, SERVER_ADDRESS))
env.warn_only = True
output['everything'] = False

class Bridge:
    """ Description """

    def __init__(self, server_password):
        env.password = server_password
        python_version = Bridge.sudo('which python')
        self.python = str(python_version)

    def send(self, path, script_file):
        """ Description """
        for file in config_file, common.__file__, script_file.__file__:
            result = put(file, path, use_sudo=True)
            msg = 'Transferred' if result.succeeded else "Not transferred"
            CMD_LOG.debug("%s: %s -> %s:%s" % (msg, file, env.host_string, path))

    def remove(self, path, only_files=False):
        """ Description """
        directory = os.path.join(path, '*') if only_files else path
        Bridge.sudo("rm -r %s" % directory)

    @staticmethod
    def remote_shell(run_with, path, script_file, exports):
        """ Description """
        file_name = os.path.basename(script_file.__file__)
        return Bridge.sudo("{prog} {path} {exports}".format(prog=run_with,
                            path=os.path.join(path, file_name), exports=','.join(exports)))

    @staticmethod
    def sudo(command):
        """ Description """
        result = sudo(command, shell=False, shell_escape=True)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], result)
        CMD_LOG.debug(result.command)
        return result
