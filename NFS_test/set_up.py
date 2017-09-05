"""
RUN WITH SUDO!!!

When set up in testing framework:
 (echo 'LOCAL=True'; cat check.py) | ssh virtual@192.168.56.5 python - server
"""

from platform import dist
import subprocess as sp
import sys
import os
import time

from constants import *


def server():
    """  """
    PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
    sp.run([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
    open(TEST_FILE_PATH, 'w').close()
    with open(EXPORTS_PATH, 'r+') as file:
        if EXPORTS_LINE not in file.readlines():
            file.write(EXPORTS_LINE)
    for util in NFS_UTILS:
        sp.run(["service", util, "restart"])

def client():
    """  """
    sp.run([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
    for util in NFS_UTILS:
        sp.run(["service", util, "start"])
    os.makedirs(CLIENT_TEST_DIR, exist_ok=True)
    sp.run([
        'mount',
        ':'.join((SERVER_ADDRESS, SERVER_TEST_DIR)),
        CLIENT_TEST_DIR
        ])


if NFS_SERVER in sys.argv:
    server()
