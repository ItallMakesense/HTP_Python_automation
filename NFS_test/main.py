""" Description """
import subprocess as sp
import logging
import sys
import os
import re

from config import *
from tear_down import remove


RUN_DIR = os.path.dirname(__file__)
if not RUN_DIR:
    RUN_DIR = os.path.dirname(os.path.abspath(__file__))

LOG = logging.getLogger(LOG_NAME)
LOG.setLevel(logging.DEBUG)
LOG_FILE = logging.FileHandler(os.path.join(RUN_DIR, LOG_DIR, LOG_NAME))
LOG_FILE.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
LOG.addHandler(LOG_FILE)

def setup_venv():
    """ Description """
    setup_order = [
        ['pip', 'install', 'virtualenv'],
        ['virtualenv', ENV_PATH],
        [PIP_PATH, 'install', 'fabric3']
        ]
    for step in setup_order:
        result = execute(step, stdout=sp.PIPE, stderr=sp.PIPE)
        write_to({LOG.debug: result[0].decode(), LOG.error: result[1].decode()})

# 0
if not CLIENT_HOST_PASSWORD:
    CLIENT_HOST_PASSWORD = input('Enter local host password: ')
if not SERVER_HOST_PASSWORD:
    SERVER_HOST_PASSWORD = input('Enter remote host password: ')

# print("LOGGER", LOG)
# 1
setup_venv()

# 2
stdout, stderr = execute(['sudo', '-S', PYTHON_PATH, os.path.join(RUN_DIR,
                         'test.py')], stdin=sp.PIPE,
                         input_line=CLIENT_HOST_PASSWORD)

################################################################################
# LOGGING + MULTIPROCESSING (I.E. SUBPROCESS) = ?!
################################################################################

# write_to({LOG.debug: stdout.decode(), LOG.error: stderr.decode()})

remove(ENV_PATH)
