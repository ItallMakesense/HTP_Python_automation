"""
Description
"""

from platform import dist
import logging
import socket
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
        for util in NFS_UTILS:
            common.execute(["service", util, "stop"])
        #
        with open(EXPORTS_PATH) as file:
            existed = file.readlines()
        if EXPORTS_LINE in existed:
            existed.remove(EXPORTS_LINE)
            with open(EXPORTS_PATH, 'w') as file:
                file.writelines(existed)
        #
        common.execute([PACKAGE_MANAGER, 'remove', '-y'] + NFS_UTILS)

    @classmethod
    def client(cls, test_dir):
        """ Description """
        remove = common.execute(['rm', '-r', test_dir], collect=True)
        #
        for util in NFS_UTILS:
            stop = common.execute(["service", util, "stop"], collect=True)
        #
        util_rem = common.execute([PACKAGE_MANAGER, 'remove', '-y'] + NFS_UTILS,
                                  collect=True)
        return remove[2] and util_rem[2]


class Case:
    """ Description """

    @classmethod
    def client(cls, test_dir):
        """ Description """
        unmount = common.execute(['umount', test_dir], collect=True)
        if unmount[2]: # Exit code
            DEBUG_LOG.debug("Unmounted - %s" % test_dir)
        return unmount[2]

if socket.gethostbyname(socket.gethostname()) == SERVER_ADDRESS:
    Suite.server(sys.argv.pop())
