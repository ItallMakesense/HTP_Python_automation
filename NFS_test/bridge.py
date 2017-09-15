"""
Module, implementing all interactions with remote host.
Provides functional, using different python package - `Fabric`, in fact being
a wrapper for that package's functional.

Includes `Bridge` class, containing functions for:
    - sending files to remote host
    - executing commands on the remote host, using superuser priviligues
"""

import os.path
import logging
from fabric.api import env, output, put, sudo

from config import *
import common


CMD_LOG = common.initiate_logger(REM_CMD_LOG)
DEBUG_LOG = logging.getLogger(DEBUG_LOG)

# Fabric variables setup
env.password = SERVER_HOST_PASSWORD
env.host_string = '@'.join((SERVER_HOST_NAME, SERVER_ADDRESS))
env.warn_only = True
env.combine_stderr = False
output['everything'] = False


class Bridge:
    """
    Holds methods for interacting with remote host, using `Fabric` package
    functional. Official docs from http://www.fabfile.org/:

    "It provides a basic suite of operations for executing local or remote
    shell commands (normally or via sudo) and uploading/downloading files,
    as well as auxiliary functionality such as prompting the running user
    for input, or aborting execution."

    Requires `server_password` during instance creation, when `self.python`
    if defined as python execution path of remote host.
    """

    def __init__(self, server_password):
        env.password = server_password
        python_version = Bridge.sudo('which python')
        self.python = str(python_version)

    def send(self, files, path):
        """
        Sends files from given `files` list to the remote host.
        Writes the result to the `CMD_LOG`
        """
        for file in files:
            result = put(file, path, use_sudo=True)
            msg = 'Transferred' if result.succeeded else "Not transferred"
            CMD_LOG.debug("%s: %s -> %s:%s" %
                          (msg, file, env.host_string, path))

    def remove(self, path, only_files=False):
        """
        Removes remote host's `path` directory, completely or content only,
        if `only_files` is `True`
        """
        directory = os.path.join(path, '*') if only_files else path
        Bridge.sudo("rm -r %s" % directory)

    @staticmethod
    def remote_shell(run_with, path, script_file, exports):
        """
        Executes `script_file` file on a remote host under the `path` directory
        with a `run_with` program (normally, python). `exports` line passed
        as last command line argument
        """
        file_name = os.path.basename(script_file.__file__)
        return Bridge.sudo("%s %s %s" % (run_with, os.path.join(path, file_name),
                                         ','.join(exports)))

    @staticmethod
    def sudo(command):
        """
        Executes given `command` with superuser's privilegues. Also writes this
        command to the `CMD_LOG`, and the result to `DEBUG_LOG`.
        Returns retrieved result
        """
        result = sudo(command)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error],
                        [result.stdout, result.stderr])
        CMD_LOG.debug(result.command)
        return result
