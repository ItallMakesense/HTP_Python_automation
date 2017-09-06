""" Description """

import os.path
import logging
from fabric.api import env, output, put, sudo

from config import SERVER_HOST_PASSWORD, SERVER_HOST_NAME, SERVER_ADDRESS,\
                   LOG_NAME, __file__ as config_file
import common


LOG = logging.getLogger(LOG_NAME)

# env.password = SERVER_HOST_PASSWORD
env.host_string = '@'.join((SERVER_HOST_NAME, SERVER_ADDRESS))
env.warn_only = True

output['everything'] = False

def prepare(path):
    """ Description """
    make_dir = sudo('mkdir %s' % path)
    common.write_to({LOG.debug: make_dir.stdout, LOG.error: make_dir.stderr})

def send(path, script_file):
    """ Description """
    for file in config_file, common.__file__, script_file.__file__:
        result = put(file, path, use_sudo=True)
        log, msg_part = (LOG.debug, 'TRANSFERRED') if result.succeeded else\
                        (LOG.error, "NOT TRANSFERRED")
        common.write_to({log: "{msg_part} - {file} - {host}:{path}".format(
            file=file, msg_part=msg_part, host=env.host_string,
            path=result.pop())})

def remote_shell(run_with, path, script_file, *args):
    """ Description """
    send(path, script_file)
    file_name = os.path.basename(script_file.__file__)
    #
    # result = sudo([run_with, '/'.join((path, file_name)), *args], shell=False)
    result = sudo("{prog} {path}/{file} {args}".format(prog=run_with, path=path,
                  file=file_name, args=' '.join(args)), pty=False, shell=False)
    common.write_to({LOG.debug: result.stdout, LOG.error: result.stderr})
