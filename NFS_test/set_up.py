"""
Module for comprehensive preparation of local and remote hosts to become
nfs client and nfs server accordingly.

Includes `Suite` class with all it's methods, serving for setup on a test class
level, and `Case` class, serving for setup on a test method level
"""

from logging import getLogger
from platform import dist
import socket
import sys
import os

from config import *
import common


DEBUG_LOG = getLogger(DEBUG_LOG)


class Suite:
    """
    Contain methods for tests setup on a test class level. These setup methods
    preparing remote host (nfs server) and local host (nfs client)
    for test execution
    """

    @classmethod
    def server(cls, exports_opts):
        """
        For nfs server: install `NFS_UTILS` packages (if available),
        writes `exports_opts` to `EXPORTS_PATH` (/etc/exports),
        export test folder with given options for nfs client
        and restart nfs utils
        """
        manager = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
        exports = JOIN_EXPORTS(exports_opts)
        for util in NFS_UTILS:
            common.execute([manager, 'install', '-y', util])
        with open(EXPORTS_PATH, 'r+') as file:
            if exports not in file.readlines():
                file.write(exports)
        common.execute(['exportfs', '-a'])
        for util in NFS_UTILS:
            common.execute(["service", util, "restart"])

    @classmethod
    def client(cls, test_dir):
        """
        For nfs client: install `NFS_UTILS` packages (if available),
        start installed nfs utils and  create `test_dir` (if not exists)
        """
        for util in NFS_UTILS:
            install = common.execute([PACKAGE_MANAGER, 'install', '-y', util],
                                     collect=True)
        for util in NFS_UTILS:
            common.execute(["service", util, "start"], collect=True)
        try:
            os.makedirs(test_dir)
        except OSError:
            pass  # When test_dir exists
        result = "Created" if os.path.exists(test_dir) else "Not created"
        DEBUG_LOG.debug("%s - %s" % (result, test_dir))
        return install[2] and True if result == "Created" else False


class Case:
    """
    Contain method for tests setup on a test method level.
    It's finish preparation of local host (nfs client)
    for separate test execution
    """

    @classmethod
    def client(cls, server_test_dir, client_test_dir):
        """ Simply mounts `server_test_dir` to the `client_test_dir` """
        remote_dir = ':'.join((SERVER_ADDRESS, server_test_dir))
        mount = common.execute(['mount', remote_dir, client_test_dir],
                               collect=True)
        if mount[2]:  # Exit code
            DEBUG_LOG.debug("Mounted - %s - %s" % (remote_dir, client_test_dir))
        return mount[2]


if socket.gethostbyname(socket.gethostname()) == SERVER_ADDRESS:
    Suite.server(sys.argv.pop())
