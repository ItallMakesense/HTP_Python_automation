"""
RUN WITH SUDO!!!

When set up in testing framework:
 (echo 'LOCAL=True'; cat check.py) | ssh virtual@192.168.56.5 python - server
"""

from platform import dist
import subprocess as sp
import sys
import os

from constants import *


def remove(directory, skip=None):
    for entry in os.scandir(directory):
        if entry.path == skip:
            continue
        elif entry.is_dir(follow_symlinks=False):
            remove(entry.path)
        else:
            os.remove(entry.path)
    os.rmdir(directory)

def server():
    """  """
    PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
    for util in NFS_UTILS:
        sp.run(["service", util, "stop"])
    with open(EXPORTS_PATH) as file:
        existed = file.readlines()
    existed.remove(EXPORTS_LINE)
    with open(EXPORTS_PATH, 'w') as file:
        file.writelines(existed)
    remove(SERVER_TEST_DIR)
    sp.run([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS])

def client():
    """  """
    sp.run(['umount', CLIENT_TEST_DIR])
    remove(CLIENT_TEST_DIR, skip=ENV_PATH)
    for util in NFS_UTILS:
        sp.run(["service", util, "stop"])
    sp.run([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS])

if NFS_SERVER in sys.argv:
    server()
