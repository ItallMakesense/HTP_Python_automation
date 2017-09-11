"""
Description
"""

from platform import dist
import subprocess as sp
import logging
import socket
import sys
import os

from config import *
import common


DEBUG_LOG = logging.getLogger(DEBUG_LOG)

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
        existed.remove(EXPORTS_LINE)
        with open(EXPORTS_PATH, 'w') as file:
            file.writelines(existed)
        #
        sp.run([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS])
        # #
        # try:
        #     remove_dir(SERVER_TEST_DIR)
        # except OSError as error:
        #     print(error)
        # else:
        #     print("Removed -", SERVER_TEST_DIR)

    @classmethod
    def client(cls, test_dir, log):
        try:
            remove_dir(test_dir, skip=ENV_DIR)
        except OSError as error:
            DEBUG_LOG.error(error)
        else:
            log.info("Removed - %s" % test_dir)
        #
        for util in NFS_UTILS:
            stop = common.execute(["service", util, "stop"], stdout=sp.PIPE, stderr=sp.PIPE)
            common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], stop)
        #
        util_rem = common.execute([PACKAGE_MANAGER, 'remove', '-y', *NFS_UTILS],
                                  stdout=sp.PIPE, stderr=sp.PIPE)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], util_rem)
        if not util_rem[2]: # Exit code
            log.info("NFS removed")


class Case:
    """ Description """

    @classmethod
    def client(cls, test_dir, log):
        """ Description """
        unmount = common.execute(['umount', test_dir], stdout=sp.PIPE, stderr=sp.PIPE)
        if not unmount[2]: # Exit code
            log.info("Unmounted - %s" % test_dir)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], unmount)

if socket.gethostbyname(socket.gethostname()) == SERVER_ADDRESS:
    Suite.server(sys.argv.pop())
