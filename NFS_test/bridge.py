""" Description """

import os.path
import logging
from fabric.api import env, output, put, sudo

import config


LOG = logging.getLogger(config.LOG_NAME)

env.password = config.SERVER_HOST_PASSWORD
env.host_string = '@'.join((config.SERVER_HOST_NAME, config.SERVER_ADDRESS))
env.warn_only = True

output['everything'] = False

def prepare(path, script_file):
    """ Description """
    script_file_path = script_file.__file__
    script_file_name = os.path.basename(script_file_path)
    #
    make_dir = sudo('mkdir %s' % path)
    config.write_to({LOG.debug: make_dir.stdout, LOG.error: make_dir.stderr})
    #
    for file in config.__file__, script_file_path:
        result = put(file, path, use_sudo=True)
        log, msg_part = (LOG.debug, 'transferred') if result.succeeded else\
                        (LOG.error, "not transferred")
        config.write_to({log: "{file} {msg_part} to {host}:{path}".format(
            file=file, msg_part=msg_part, host=env.host_string,
            path=result.pop())})
    return script_file_name

def remote_shell(run_with, path, script_file, *args):
    """ Description """
    script_file_name = prepare(path, script_file)
    result = sudo("{prog} {path}/{file} {args}".format(
        prog=run_with, path=path, file=script_file_name, args=' '.join(args)))
    config.write_to({LOG.debug: result.stdout, LOG.error: result.stderr})
