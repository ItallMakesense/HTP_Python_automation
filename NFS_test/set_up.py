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


def server():
    """ Description """
    PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
    #
    execute([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
    # sp.run([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
    #
    open(TEST_FILE_PATH, 'w').close()
    #
    with open(EXPORTS_PATH, 'r+') as file:
        if EXPORTS_LINE not in file.readlines():
            file.write(EXPORTS_LINE)
    #
    for util in NFS_UTILS:
        execute(["service", util, "restart"])
        # sp.run(["service", util, "restart"])

def client():
    """ Description """
    LOG = logging.getLogger(LOG_NAME)
    #
    install = execute([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS],
                      stdout=sp.PIPE, stderr=sp.PIPE)
    write_to({LOG.debug: install[0].decode(), LOG.error: install[1].decode()})
    # sp.run([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
    #
    for util in NFS_UTILS:
        start = execute(["service", util, "start"], stdout=sp.PIPE,
                        stderr=sp.PIPE)
        write_to({LOG.debug: start[0].decode(), LOG.error: start[1].decode()})
        # sp.run(["service", util, "start"])
    #
    os.makedirs(CLIENT_TEST_DIR, exist_ok=True)
    if os.path.exists(CLIENT_TEST_DIR):
        log, msg = LOG.debug, ' '.join((CLIENT_TEST_DIR, "created"))
    else:
        log, msg = LOG.error, ' '.join((CLIENT_TEST_DIR, "not created"))
    write_to({log: msg})
    #
    mount = execute(['mount', ':'.join((SERVER_ADDRESS, SERVER_TEST_DIR)),
                     CLIENT_TEST_DIR], stdout=sp.PIPE, stderr=sp.PIPE)
    write_to({LOG.debug: mount[0].decode(), LOG.error: mount[1].decode()})
    # sp.run([
    #     'mount',
    #     ':'.join((SERVER_ADDRESS, SERVER_TEST_DIR)),
    #     CLIENT_TEST_DIR
    #     ])

if NFS_SERVER in sys.argv:
    server()
