"""
DESCRIPTION
"""

from platform import dist
from subprocess import check_output, CalledProcessError
import os

# Root directory of `nfs tester`
_file_dir_ = os.path.dirname(__file__)

# Logs constants
LOG_DIR = os.path.join(_file_dir_, 'logs') # Write desirable folder
INFO_LOG = 'info.log' # Write desirable name
DEBUG_LOG = 'debug.log' # Write desirable name
CMD_LOG = 'ssh_cmds.log' # Write desirable name

# Required tools
try: # When pip isn't installed on a computer, where module is
    SHELL_PIP = check_output('which pip', shell=True).decode().strip()
except  CalledProcessError:
    SHELL_PIP = None


# Virtual environment constants
ENV_DIR = os.path.join(_file_dir_, 'venv') # Write desirable folder
ENV_PIP = os.path.join(ENV_DIR, 'bin/pip')
ENV_PYTHON = os.path.join(ENV_DIR, 'bin/python')

# Server info
SERVER_ADDRESS = '192.168.1.4' # Write server address
SERVER_HOST_NAME = 'virtual' # Write server user
SERVER_HOST_PASSWORD = None # Write server sudo password (also see `pytest_nfs.py`)

# Client info
CLIENT_UID = os.geteuid()
CLIENT_GID = os.getegid()
CLIENT_ADDRESS = '192.168.1.2' # Write client address
CLIENT_HOST_PASSWORD = None # Write server sudo password (also see `pytest_nfs.py`)

# Testing folders
SERVER_TEST_DIR = '/mnt/future_test' # Write desirable folder
CLIENT_TEST_DIR = '/mnt/future_test' # Write desirable folder

# Exports info
EXPORTS_PATH = '/etc/exports'
EXPORTS_OPTIONS = ['sync', 'no_subtree_check'] # Example. Will change in every test case
JOIN_EXPORTS = lambda options: "{dir} {ip}({opt})\n".format(
    dir=SERVER_TEST_DIR,
    ip=CLIENT_ADDRESS,
    opt=options
    ) # Makes exports line from arguments

# Dictionary containing appropriate package managers for different distributives
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
PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()] # Contains PMs name of the current OS
NFS_UTILS = ['nfs-kernel-server', 'nfs-common']

# command line arguments = {
CLIENT_PASS = '--client_pass'
SERVER_PASS = '--server_pass'
# }

__all__ = [const for const in dir() if not const.startswith('_')]
