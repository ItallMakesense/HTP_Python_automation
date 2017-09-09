"""
Description
"""

from platform import dist
import subprocess as sp
import logging
import sys
import os

from config import *
import common


DEBUG_LOG = logging.getLogger(DEBUG_LOG)

class Suite:
    """ Description """

    @classmethod
    def server(cls, exports_opts):
        """ Description """
        PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
        EXPORTS_LINE = JOIN_EXPORTS(exports_opts)
        #
        common.execute([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS])
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
    def client(cls, test_dir, log):
        """ Description """
        install = common.execute([PACKAGE_MANAGER, 'install', '-y', *NFS_UTILS],
                                 stdout=sp.PIPE, stderr=sp.PIPE)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], install)
        #
        for util in NFS_UTILS:
            start = common.execute(["service", util, "start"], stdout=sp.PIPE,
                                   stderr=sp.PIPE)
            common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], start)
        if not start[2]: # Exit code
            log.info("NFS installed")
        #
        os.makedirs(test_dir, exist_ok=True)
        if os.path.exists(test_dir):
            log.info("Created - %s" % test_dir)
        else:
            DEBUG_LOG.debug("Not created - %s" % test_dir)

class Case:
    """ Description """

    @classmethod
    def client(cls, test_dir, log):
        """ Description """
        remote_dir = ':'.join((SERVER_ADDRESS, SERVER_TEST_DIR))
        mount = common.execute(['mount', remote_dir, test_dir], stdout=sp.PIPE,
                               stderr=sp.PIPE)
        if not mount[2]: # Exit code
            log.info("Mounted - %s - %s" % (remote_dir, test_dir))
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], mount)

if NFS_SERVER in sys.argv:
    Suite.server(sys.argv.pop())
