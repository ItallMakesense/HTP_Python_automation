"""
Description
"""

from __future__ import print_function
from platform import dist
from subprocess import PIPE
from logging import getLogger
import socket
import sys
import os

from config import *
import common


DEBUG_LOG = getLogger(DEBUG_LOG)

class Suite:
    """ Description """

    @classmethod
    def server(cls, exports_opts):
        """ Description """
        PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
        EXPORTS_LINE = JOIN_EXPORTS(exports_opts)
        #
        common.execute([PACKAGE_MANAGER, 'install', '-y'] + NFS_UTILS)
        #
        with open(EXPORTS_PATH, 'r+') as file:
            if EXPORTS_LINE not in file.readlines():
                file.write(EXPORTS_LINE)
        #
        common.execute(['exportfs', '-a'])
        #
        for util in NFS_UTILS:
            common.execute(["service", util, "restart"])

    @classmethod
    def client(cls, test_dir):
        """ Description """
        install = common.execute([PACKAGE_MANAGER, 'install', '-y'] + NFS_UTILS,
                                 collect=True)
        # common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], install)
        #
        for util in NFS_UTILS:
            start = common.execute(["service", util, "start"], collect=True)
            # common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], start)
        try:
            os.makedirs(test_dir)
        except OSError:
            pass # When test_dir exists
        result = "Created" if os.path.exists(test_dir) else "Not created"
        DEBUG_LOG.debug("%s - %s" % (result, test_dir))
        return install[2] and True if result == "Created" else False

class Case:
    """ Description """

    @classmethod
    def client(cls, test_dir):
        """ Description """
        remote_dir = ':'.join((SERVER_ADDRESS, SERVER_TEST_DIR))
        mount = common.execute(['mount', remote_dir, test_dir], collect=True)
        if mount[2]: # Exit code
            DEBUG_LOG.debug("Mounted - %s - %s" % (remote_dir, test_dir))
        # common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], mount)
        return mount[2]

if socket.gethostbyname(socket.gethostname()) == SERVER_ADDRESS:
    Suite.server(sys.argv.pop())
