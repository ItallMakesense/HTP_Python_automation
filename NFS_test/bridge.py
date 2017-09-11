""" Description """

import os.path
import logging
from fabric.api import env, output, put, sudo

from config import *
from config import __file__ as config_file
import common


DEBUG_LOG = logging.getLogger(DEBUG_LOG)

env.password = SERVER_HOST_PASSWORD
env.host_string = '@'.join((SERVER_HOST_NAME, SERVER_ADDRESS))
env.warn_only = True

output['everything'] = False


class Bridge:

    def __init__(self, suite):
        env.password = suite.server_password
        self.__class__.log = suite.log

    @staticmethod
    def prepare(path):
        """ Description """
        make_dir = sudo('mkdir %s' % path, shell=False, shell_escape=True)
        if make_dir.succeeded:
            Bridge.log.info("Created - %s" % path)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], make_dir)

    @staticmethod
    def send(path, script_file):
        """ Description """
        for file in config_file, common.__file__, script_file.__file__:
            result = put(file, path, use_sudo=True)
            log, msg_part = (Bridge.log.info, 'Transferred') if result.succeeded\
                             else (DEBUG_LOG.debug, "Not transferred")
            log("{msg_part} - {file} - {host}:{path}".format(file=file,
                msg_part=msg_part, host=env.host_string, path=result.pop()))

    @staticmethod
    def remove(path, only_files=False):
        directory = os.path.join(path, '*') if only_files else path
        remove = sudo("rm -r %s" % directory, shell=False, shell_escape=True)
        if remove.succeeded:
            Bridge.log.info("Removed - %s" % SERVER_TEST_DIR)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], remove)

    @staticmethod
    def remote_shell(run_with, path, script_file, *args):
        """ Description """
        # Execute setup files
        file_name = os.path.basename(script_file.__file__)
        result = sudo("{prog} {file_path} {args}".format(prog=run_with,
                    file_path=os.path.join(path, file_name), args=' '.join(args)),
                    shell=False, shell_escape=True)
        return result

    @staticmethod
    def sudo(cmd):
        return sudo(cmd, shell=False, shell_escape=True)


def prepare(path, logger):
    """ Description """
    make_dir = sudo('mkdir %s' % path, shell=False, shell_escape=True)
    if make_dir.succeeded:
        logger.info("Created - %s" % path)
    common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], make_dir)

def send(path, script_file, logger):
    """ Description """
    for file in config_file, common.__file__, script_file.__file__:
        result = put(file, path, use_sudo=True)
        log, msg_part = (logger.info, 'Transferred') if result.succeeded else\
                        (DEBUG_LOG.debug, "Not transferred")
        log("{msg_part} - {file} - {host}:{path}".format(file=file,
            msg_part=msg_part, host=env.host_string, path=result.pop()))

def remove(path, logger, only_files=False):
    directory = os.path.join(path, '*') if only_files else path
    remove = sudo("rm -r %s" % directory, shell=False, shell_escape=True)
    if remove.succeeded:
        logger.info("Removed - %s" % SERVER_TEST_DIR)
    common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], remove)

def remote_shell(run_with, path, script_file, *args):
    """ Description """
    # Execute setup files
    file_name = os.path.basename(script_file.__file__)
    result = sudo("{prog} {file_path} {args}".format(prog=run_with,
                   file_path=os.path.join(path, file_name), args=' '.join(args)),
                   shell=False, shell_escape=True)
    return result
