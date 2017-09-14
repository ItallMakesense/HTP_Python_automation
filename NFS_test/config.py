"""
Configurational module for `NFS_test` package.

Defines almost all constants, used by other modules, including:
    - Name of the folder, containing log files
    - Name of each log, that will be created during testing
    - Path to the local host's pip package manager
    - Path, where virtual environment will be installed
    - Remote and local host's information
    - Paths to local and remote test folders
    - Names of file and user, that will be created during testing
    - Path to exports file on a remote host, and options, that will be written
      to this file, for every test case
    - Names of linux package managers, different for various distributions
    - Names of nfs setup utils
    - Command line argument names, used by `conftest.py`
"""

from platform import dist
from subprocess import check_output, CalledProcessError
import os


# Root directory of `nfs test` package
_file_dir_ = os.path.dirname(__file__)

# Logs constants (Rewrite if needed)
LOG_DIR = os.path.join(_file_dir_, 'logs')
INFO_LOG = 'info.log' # Contains general test running information
DEBUG_LOG = 'debug.log' # Contains more information, including errors
LOC_CMD_LOG = 'loc_cmd.log' # Contain commands, executed on the local host
REM_CMD_LOG = 'rem_cmd.log' # Contain sent direct commands for the remote host
# Same but for tests
OWN_TEST_LOG = 'test_owner.log'
RO_TEST_LOG = 'test_ro_access.log'
RW_TEST_LOG = 'test_rw_access.log'

# Pip manager. Required to de defined only in main `pytest_nfs` module
try: # When pip isn't installed, where this module is located
    SHELL_PIP = check_output('which pip', shell=True).decode().strip()
except  CalledProcessError:
    SHELL_PIP = None

# Virtual environment constants
ENV_DIR = os.path.join(_file_dir_, 'venv') # Write desirable folder
# Filled automatically
ENV_PIP = os.path.join(ENV_DIR, 'bin/pip')
ENV_PYTHON = os.path.join(ENV_DIR, 'bin/python')

# Server side info (Rewrite if needed)
SERVER_ADDRESS = '200.100.50.25'
SERVER_HOST_NAME = 'server'
SERVER_HOST_PASSWORD = None

# Client side info (Rewrite if needed)
CLIENT_ADDRESS = '100.10.1.0'
CLIENT_HOST_PASSWORD = None

# Testing parameters (Rewrite if needed)
SERVER_TEST_DIR = '/mnt/test_nfs'
CLIENT_TEST_DIR = '/mnt/test_nfs'
TEST_FILE = 'test_file'
TEST_USER = 'test_user'

# Exports info (Rewrite if needed)
EXPORTS_PATH = '/etc/exports'
RW_EXPORTS = ['rw', 'sync', 'no_root_squash', 'no_subtree_check']
RO_EXPORTS = ['ro', 'sync', 'no_root_squash', 'no_subtree_check']
OWN_EXPORTS = ['rw', 'sync', 'anonuid=%s' % os.geteuid(),
               'anongid=%s' % os.getegid(), 'no_subtree_check']
# Makes exports line from arguments
JOIN_EXPORTS = lambda options: "{dir} {ip}({opt})\n".format(
    dir=os.path.dirname(__file__),
    ip=CLIENT_ADDRESS,
    opt=options
    )

# Dictionary containing appropriate package managers for different distributives
PACKAGE_MANAGERS_MAP = {
    'debian': 'apt-get',
    'ubuntu': 'apt-get',
    'centos': 'yum',
    'redhat': 'yum'
    }
# Contains PMs name of the current OS
PACKAGE_MANAGER = PACKAGE_MANAGERS_MAP[dist()[0].lower()]
# Names of nfs packages, that can be available to linux distributives
NFS_UTILS = ['nfs-utils', 'nfs-kernel-server', 'nfs-common']

# Command line arguments. Used in `conftest.py` and `pytest_nfs.py`
LOC_PASS_OP = '--client_pass'
REM_PASS_OP = '--server_pass'
LOC_DIR_OP = '--client_dir'
REM_DIR_OP = '--server_dir'
TEST_FILE_OP = '--test_file'
TEST_USER_OP = '--test_user'

__all__ = [const for const in dir() if not const.startswith('_')]
