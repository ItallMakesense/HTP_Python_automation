"""
Description
"""

from platform import dist
import subprocess as sp
import sys
import os

from config import *
import common


def remove_dir(directory, skip=None):
    """ Description """
    for entry in os.scandir(directory):
        if entry.path == skip:
            continue
        elif entry.is_dir(follow_symlinks=False):
            remove_dir(entry.path)
        else:
            os.remove(entry.path)
    os.rmdir(directory)

def server(exports_opts):
    """ Description """
    PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
    EXPORTS_LINE = JOIN_EXPORTS(exports_opts)
    #
    for util in NFS_UTILS:
        common.execute(["service", util, "stop"])
    #
    with open(EXPORTS_PATH) as file:
        existed = file.readlines()
    existed.remove(EXPORTS_LINE)
    with open(EXPORTS_PATH, 'w') as file:
        file.writelines(existed)
    #
    sp.run([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS])
    #
    try:
        remove_dir(SERVER_TEST_DIR)
    except OSError as error:
        print(error)
    else:
        print("Removed -", SERVER_TEST_DIR)

def client(logger):
    """ Description """
    LOG = logger
    #
    unmount = common.execute(['umount', CLIENT_TEST_DIR], stdout=sp.PIPE, stderr=sp.PIPE)
    common.write_to({LOG.debug: unmount[0].decode(), LOG.error: unmount[1].decode()})
    #
    try:
        remove_dir(CLIENT_TEST_DIR, skip=ENV_PATH)
    except OSError as error:
        common.write_to({LOG.error: error})
    else:
        common.write_to({LOG.debug: ' '.join(("Removed -", CLIENT_TEST_DIR))})
    #
    for util in NFS_UTILS:
        stop = common.execute(["service", util, "stop"], stdout=sp.PIPE, stderr=sp.PIPE)
        common.write_to({LOG.debug: stop[0].decode(), LOG.error: stop[1].decode()})
    #
    util_rem = common.execute([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS],
                              stdout=sp.PIPE, stderr=sp.PIPE)
    common.write_to({LOG.debug: util_rem[0].decode(), LOG.error: util_rem[1].decode()})

if NFS_SERVER in sys.argv:
    server(sys.argv.pop())
