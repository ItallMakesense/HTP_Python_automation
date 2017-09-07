""" Description """

import os.path
from fabric.api import env, output, put, sudo

from config import SERVER_HOST_PASSWORD, SERVER_HOST_NAME, SERVER_ADDRESS,\
                   LOG_NAME, __file__ as config_file
import common


env.password = SERVER_HOST_PASSWORD
env.host_string = '@'.join((SERVER_HOST_NAME, SERVER_ADDRESS))
env.warn_only = True

output['everything'] = False

# def use_logger(logger):
#     def for_this(function):
#         def wrapper(*a):
#             LOG = logger
#             return function(*a)
#         return wrapper
#     return for_this


def prepare(logger, path):
    """ Description """
    LOG = logger
    make_dir = sudo('mkdir %s' % path, shell=False, shell_escape=True)
    common.write_to({LOG.debug: make_dir.stdout, LOG.error: make_dir.stderr})

def send(logger, path, script_file):
    """ Description """
    LOG = logger
    for file in config_file, common.__file__, script_file.__file__:
        result = put(file, path, use_sudo=True)
        log, msg_part = (LOG.debug, 'Transferred') if result.succeeded else\
                        (LOG.error, "Not transferred")
        common.write_to({log: "{msg_part} - {file} - {host}:{path}".format(
            file=file, msg_part=msg_part, host=env.host_string,
            path=result.pop())})

def remote_shell(logger, run_with, path, script_file, *args):
    """ Description """
    LOG = logger
    send(LOG, path, script_file)
    file_name = os.path.basename(script_file.__file__)
    #
    result = sudo("{prog} {file_path} {args}".format(prog=run_with,
                   file_path=os.path.join(path, file_name), args=' '.join(args)),
                   shell=False, shell_escape=True)
    common.write_to({LOG.debug: result.stdout, LOG.error: result.stderr})
