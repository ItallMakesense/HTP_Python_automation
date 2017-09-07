"""
DESCRIPTION
"""

import subprocess as sp
import logging
import os.path

from config import LOG_DIR, LOG_NAME


def execute(command, stdin=None, stdout=None, stderr=None, input_line=None):
    """ Description """
    shell = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, start_new_session=True)
    if input_line:
        input_line = (input_line + '\n').encode()
    return shell.communicate(input=input_line)

def write_to(msg_to_log_map):
    """
    This function fiters empty lines in the given `msg` string,
    and logs the rest to the given `log` logger, line by line
    """
    for log, msg in msg_to_log_map.items():
        for line in msg.splitlines():
            if line:
                log(line)

def initiate_logger(name, file):
    """ Description """
    directory = os.path.dirname(file)
    if not directory:
        directory = os.path.dirname(os.path.abspath(file))
    #
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log_file = logging.FileHandler(os.path.join(directory, LOG_DIR, name))
    log_file.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
    log.addHandler(log_file)
    return directory, log, log_file

MAKE_CAP = lambda string: string.upper().center(80, '=')
