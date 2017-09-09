"""
DESCRIPTION
"""

from platform import dist
import os


_file_dir_ = os.path.dirname(__file__)

LOG_DIR = os.path.join(_file_dir_, 'logs') # Write desirable directory
INFO_LOG = 'info.log'
DEBUG_LOG = 'debug.log'
CMD_LOG = 'commands.log'

ENV_DIR = os.path.join(_file_dir_, 'venv') # Write desirable directory
PIP_PATH = os.path.join(ENV_DIR, 'bin/pip')
PYTHON_PATH = os.path.join(ENV_DIR, 'bin/python')

NFS_SERVER = 'server'

SERVER_HOST_NAME = 'virtual' # Write known name
SERVER_HOST_PASSWORD = 'me' # Write known password
SERVER_ADDRESS = '192.168.56.5' # Write known address

# CLIENT_HOST_NAME
CLIENT_HOST_PASSWORD = 'me'
CLIENT_ADDRESS = '192.168.56.1'

SERVER_TEST_DIR = '/mnt/future_test' # Write desirable directory
CLIENT_TEST_DIR = '/mnt/future_test' # Write desirable directory

# TEST_FILE = 'test_file' # Write desirable file name
# GET_TEST_PATH = lambda test_dir: os.path.join(test_dir, TEST_FILE)
TESTS_DIR = os.path.join(_file_dir_, 'tests')


EXPORTS_PATH = '/etc/exports'
EXPORTS_OPTIONS = ['sync', 'no_subtree_check'] # Example. Will change in every test case
JOIN_EXPORTS = lambda options: "{dir} {ip}({opt})\n".format(
    dir=SERVER_TEST_DIR,
    ip=CLIENT_ADDRESS,
    opt=options
    )

PACKAGE_MANAGERS_MAP = {
    'debian': 'apt-get',
    'ubuntu': 'apt-get',
    'centos': 'yum',
    'redhat': 'yum',
    'yellowdog': 'yum',
    'suse': 'zypper',
    'fedora': 'dnf',
    'gentoo': 'equo'
    }
PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]

NFS_UTILS = ('nfs-kernel-server', 'nfs-common')

__all__ = [const for const in dir() if not const.startswith('_')]
