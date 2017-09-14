"""
Module serves for restoring all the initial conditions, that was before the
appropriate setup of nfs server-client system, made by `set_up.py` module.

Includes `Suite` class with all it's methods, serving for teardown on a test
class level, and `Case` class, serving for teardown on a test method level
"""

from platform import dist
import logging
import socket
import sys

from config import *
import common


DEBUG_LOG = logging.getLogger(DEBUG_LOG)


class Suite:
    """
    Contain methods for tests teardown on a test class level.
    These setup methods removing all of the changes, made on remote host
    (nfs server) and local host (nfs client) for test execution
    """

    @classmethod
    def server(cls, exports_opts):
        """
        For nfs server: stop all the installed `NFS_UTILS`,
        remove all the exports, including `exports_opts`, from `EXPORTS_PATH`
        (/etc/exports) and remove `NFS_UTILS` packages (again, if installed)
        """
        manager = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
        exports = JOIN_EXPORTS(exports_opts)
        for util in NFS_UTILS:
            common.execute(["service", util, "stop"])
        with open(EXPORTS_PATH) as file:
            existed = file.readlines()
        if exports in existed:
            existed.remove(exports)
            with open(EXPORTS_PATH, 'w') as file:
                file.writelines(existed)
        for util in NFS_UTILS:
            common.execute([manager, 'remove', '-y', util])

    @classmethod
    def client(cls, test_dir):
        """
        For nfs client: remove `test_dir`, stop all the installed `NFS_UTILS`
        and then remove them
        """
        remove = common.execute(['rm', '-r', test_dir], collect=True)
        for util in NFS_UTILS:
            common.execute(["service", util, "stop"], collect=True)
        for util in NFS_UTILS:
            util_rem = common.execute([PACKAGE_MANAGER, 'remove', '-y', util],
                                      collect=True)
        return remove[2] and util_rem[2]


class Case:
    """
    Contain method for tests teardown on a test method level.
    It's restore conditions, that was before `set_up.Case.client`
    method execution
    """

    @classmethod
    def client(cls, test_dir):
        """ Simply unmounts `test_dir` """
        unmount = common.execute(['umount', test_dir], collect=True)
        if unmount[2]:  # Exit code
            DEBUG_LOG.debug("Unmounted - %s" % test_dir)
        return unmount[2]


if socket.gethostbyname(socket.gethostname()) == SERVER_ADDRESS:
    Suite.server(sys.argv.pop())
