"""
RUN WITH SUDO!!!

When set up in testing framework:
 (echo 'LOCAL=True'; cat check.py) | ssh virtual@192.168.56.5 python - server
"""

from platform import dist
import subprocess as sp
import logging
import sys
import os

from config import *


def remove(directory, skip=None):
    """ Description """
    for entry in os.scandir(directory):
        if entry.path == skip:
            continue
        elif entry.is_dir(follow_symlinks=False):
            remove(entry.path)
        else:
            os.remove(entry.path)
    os.rmdir(directory)

def server():
    """ Description """
    PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
    #
    for util in NFS_UTILS:
        execute(["service", util, "stop"])
        # sp.run(["service", util, "stop"])
    #
    with open(EXPORTS_PATH) as file:
        existed = file.readlines()
    existed.remove(EXPORTS_LINE)
    with open(EXPORTS_PATH, 'w') as file:
        file.writelines(existed)
    #
    remove(SERVER_TEST_DIR)
    #
    sp.run([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS])

def client():
    """ Description """
    LOG = logging.getLogger(LOG_NAME)
    #
    unmount = execute(['umount', CLIENT_TEST_DIR], stdout=sp.PIPE,
                      stderr=sp.PIPE)
    write_to({LOG.debug: unmount[0].decode(), LOG.error: unmount[1].decode()})
    # sp.run(['umount', CLIENT_TEST_DIR])
    #
    try:
        remove(CLIENT_TEST_DIR, skip=ENV_PATH)
    except OSError as error:
        write_to({LOG.error: error})
    else:
        write_to({LOG.debug: ' '.join((CLIENT_TEST_DIR, "was removed"))})
    #
    for util in NFS_UTILS:
        stop = execute(["service", util, "stop"], stdout=sp.PIPE,
                       stderr=sp.PIPE)
        write_to({LOG.debug: stop[0].decode(), LOG.error: stop[1].decode()})
        # sp.run(["service", util, "stop"])
    #
    util_rem = execute([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS],
                       stdout=sp.PIPE, stderr=sp.PIPE)
    write_to({LOG.debug: util_rem[0].decode(), LOG.error: util_rem[1].decode()})
    # sp.run([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS])

if NFS_SERVER in sys.argv:
    server()
