"""
DESCRIPTION
"""

import subprocess as sp
import logging
import os.path

from config import *

# Used for getting log's headers
MAKE_CAP = lambda string, filler='=': string.upper().center(80, filler)

def execute(command, stdin=None, stdout=None, stderr=None, shell=False,
            input_line=None):
    """ Description """
    shell = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr,
                     shell=shell, start_new_session=True)
    if input_line:
        input_line = (input_line + '\n').encode()
    try:
        stdout, stderr = shell.communicate(input=input_line)
    except KeyboardInterrupt as exc:
        sp.run(['sudo', '-S', 'kill', str(shell.pid)], input=input_line)
        stdout, stderr = "Interrupted".encode(), repr(exc).encode()
    return stdout, stderr, shell.returncode

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
    os.makedirs(LOG_DIR, exist_ok=True)
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log_file = logging.FileHandler(os.path.join(LOG_DIR, name))
    log_file.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s"))
    log.addHandler(log_file)
    return log, log_file
