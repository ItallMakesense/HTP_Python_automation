"""
Description
"""

from platform import dist
import subprocess as sp
import sys
import os

from config import *
import common


def server(exports_opts):
    """ Description """
    PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
    EXPORTS_LINE = JOIN_EXPORTS(exports_opts)
    TEST_FILE_PATH = GET_TEST_PATH(SERVER_TEST_DIR)
    #
    common.execute([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
    #
    open(TEST_FILE_PATH, 'w').close()
    if os.path.exists(TEST_FILE_PATH):
        print("Created -", TEST_FILE_PATH)
    else:
        print("Not created -", TEST_FILE_PATH)
    #
    with open(EXPORTS_PATH, 'r+') as file:
        if EXPORTS_LINE not in file.readlines():
            file.write(EXPORTS_LINE)
    #
    common.execute(['exportfs', '-a'])
    #
    for util in NFS_UTILS:
        common.execute(["service", util, "restart"])

def client(logger):
    """ Description """
    LOG = logger
    #
    install = common.execute([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS],
                             stdout=sp.PIPE, stderr=sp.PIPE)
    common.write_to({LOG.debug: install[0].decode(), LOG.error: install[1].decode()})
    #
    for util in NFS_UTILS:
        start = common.execute(["service", util, "start"], stdout=sp.PIPE,
                               stderr=sp.PIPE)
        common.write_to({LOG.debug: start[0].decode(), LOG.error: start[1].decode()})
    #
    os.makedirs(CLIENT_TEST_DIR, exist_ok=True)
    if os.path.exists(CLIENT_TEST_DIR):
        log, msg = LOG.debug, ' '.join(("Created -", CLIENT_TEST_DIR,))
    else:
        log, msg = LOG.error, ' '.join(("Not created -", CLIENT_TEST_DIR))
    common.write_to({log: msg})
    #
    mount = common.execute(['mount', '-o', '_netdev', ':'.join((SERVER_ADDRESS, SERVER_TEST_DIR)),
                            CLIENT_TEST_DIR], stdout=sp.PIPE, stderr=sp.PIPE)
    common.write_to({LOG.debug: mount[0].decode(), LOG.error: mount[1].decode()})

if NFS_SERVER in sys.argv:
    server(sys.argv.pop())
