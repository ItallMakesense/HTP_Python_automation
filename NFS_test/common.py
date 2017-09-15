"""
Module, containing functions, widely used by other modules of this package.

Includes functions for:
    - execution of commands through a separate subprocess
    - writing messages to logs
    - initiating new logs
"""

import subprocess as sp
import logging
import os

from config import *


DEBUG_LOG = logging.getLogger(DEBUG_LOG)
CMD_LOG = logging.getLogger(LOC_CMD_LOG)

# Creates log's headers, filled with `filler` from both sides of the `string`
MAKE_CAP = lambda string, filler='=': string.upper().center(80, filler)


def execute(command, shell=False, collect=False, input_line=None, pytest=False,
            secure=[]):
    """
    Wrapper around `subprocess.Popen` function. Writes linux `command` to the
    `CMD_LOG` logger, runs this command, writes `input_line` (if it's given)
    to stdin, and returns received stdout with stderr, if `collect` is `True`.
    Also writes these streams, if there was any and if `pytest` is `False`,
    to the `DEBUG_LOG`
    """
    # variables
    stdin = sp.PIPE if input_line else None
    stdout, stderr = (sp.PIPE,) * 2 if collect else (None,) * 2
    password = (input_line + '\n').encode() if input_line else None
    # process creation
    proc = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr,
                    shell=shell, preexec_fn=os.setsid)
    # logging
    if secure:
        command = command.split() if shell else command
        command = [c if c not in secure else '*'*len(c) for c in command]
    CMD_LOG.debug(command if shell else ' '.join(command))
    # execution
    try:
        output, errors = proc.communicate(input=password)
    except KeyboardInterrupt:
        return execute(['sudo', '-S', 'kill', str(proc.pid)], collect=True,
                       input_line=input_line)
    if collect and not pytest:
        write_to([DEBUG_LOG.debug, DEBUG_LOG.error], [output, errors])
    return output, errors, not proc.returncode


def write_to(loggers, msg):
    """
    Writes `msg` to every logger in the given `loggers`,
    if message is one string. If message is combined from two
    (normally stdout and stderr), first member goes to the first logger,
    and second - to the second
    """
    def split_and_log(logger, msg):
        """
        Fiters empty lines in the given `msg` string,
        and writes the rest to the given `logger`, line by line
        """
        for line in msg.splitlines():
            if line:
                logger(line)
    if isinstance(msg, str):
        for logger in loggers:
            logger(msg)
    elif isinstance(msg, list):
        for logger, part in zip(loggers, msg):
            part = part if not isinstance(part, bytes) else part.decode()
            split_and_log(logger, part)


def initiate_logger(name, with_file=False):
    """
    Cretes folder for logs (if not exists) and activates logger from `logging`
    module, returning this logger (and it's file, if `with_file` is `True`)
    """
    try:
        os.makedirs(LOG_DIR)
    except OSError:
        pass  # Mostly here, when LOG_DIR exists
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log_file = logging.FileHandler(os.path.join(LOG_DIR, name))
    log_file.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s"))
    log.addHandler(log_file)
    return (log, log_file) if with_file else log
