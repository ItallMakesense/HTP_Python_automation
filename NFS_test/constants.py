"""
DESCRIPTION
"""

from platform import dist
import socket
import os


ENV_DIR = os.getcwd() # Write desirable directory

ENV_NAME = 'new' # Write desirable name

ENV_PATH = os.path.join(ENV_DIR, ENV_NAME)
PIP_PATH = os.path.join(ENV_PATH, 'bin/pip')
PYTHON_PATH = os.path.join(ENV_PATH, 'bin/python')

NFS_SERVER = 'server'

SERVER_HOST_NAME = 'virtual' # Write known name
SERVER_HOST_PASSWORD = 'me' # Write known password
SERVER_ADDRESS = '192.168.56.5' # Write known address

# CLIENT_HOST_NAME
CLIENT_HOST_PASSWORD = 'me'
CLIENT_ADDRESS = '192.168.56.1'

SERVER_TEST_DIR = '/mnt/future_test' # Write desirable directory
CLIENT_TEST_DIR = '/mnt/future_test' # Write desirable directory

TEST_FILE_NAME = 'test_file' # Write desirable file name
TEST_FILE_PATH = os.path.join(SERVER_TEST_DIR, TEST_FILE_NAME)


EXPORTS_PATH = '/etc/exports'
EXPORTS_OPTIONS = ['rw', 'sync', 'no_root_squash']
EXPORTS_LINE = "{dir} {ip}({opt})\n".format(
    dir=SERVER_TEST_DIR,
    ip=CLIENT_ADDRESS,
    opt=','.join(EXPORTS_OPTIONS)
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
