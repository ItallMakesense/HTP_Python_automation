"""
DESCRIPTION
"""

import subprocess as sp
import logging
import os

from config import *


DEBUG_LOG = logging.getLogger(DEBUG_LOG)

# Used for getting log's headers
MAKE_CAP = lambda string, filler='=': string.upper().center(80, filler)

def execute(command, collect=False, input_line=None, pytest=False):
    """ Description """
    # variables
    command = command if isinstance(command, str) else ' '.join(command)
    stdin = sp.PIPE if input_line else None
    stdout, stderr = (sp.PIPE,)*2 if collect else (None,)*2
    password = (input_line + '\n').encode() if input_line else None
    # execution
    proc = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, shell=True,
                    preexec_fn=os.setsid)
    try:
        output, errors = proc.communicate(input=password)
    except KeyboardInterrupt:
        execute('sudo -S kill %s' % str(proc.pid), input_line=input_line)
        output, errors = proc.stdout.read(), proc.stderr.read()
    if collect and not pytest:
        write_to([DEBUG_LOG.debug, DEBUG_LOG.error],
                 (output, errors, proc.returncode))
    return output, errors, not proc.returncode

def write_to(loggers, msg):
    """
    This function fiters empty lines in the given `msg` string,
    and logs the rest to the given `log` logger, line by line
    """
    def split_and_log(logger, msg):
        """ Description """
        for line in msg.splitlines():
            if line:
                logger(line)
    std_map = {0: 'stdout', 1: 'stderr'}
    for num, logger in enumerate(loggers):
        if isinstance(msg, str):
            split_and_log(logger, msg)
        elif isinstance(msg, tuple):
            split_and_log(logger, msg[num].decode()) # stdout - 0, stderr - 1
        else:
            split_and_log(logger, getattr(msg, std_map[num]))

def initiate_logger(name):
    """ Description """
    try:
        os.makedirs(LOG_DIR)
    except OSError:
        pass # Mostly here, when LOG_DIR exists
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log_file = logging.FileHandler(os.path.join(LOG_DIR, name))
    log_file.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s"))
    log.addHandler(log_file)
    return log, log_file
