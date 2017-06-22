"""
This module is used, as constants hub (also keeps one useful function)
"""

from platform import linux_distribution
from os.path import expanduser
from os import getcwd
import socket
import os


server_name = socket.gethostname()
server_address = socket.gethostbyname(server_name)
server_password = 'me'
client_username = 'virtual'
client_address = '192.168.1.3'
client_password = 'me'

home_path = expanduser('~')
linux = linux_distribution(full_distribution_name=0)[0]

packages = {
    'debian': 'apt-get',
    'ubuntu': 'apt-get',
    'centos': 'yum',
    'redhat': 'yum',
    'yellowdog': 'yum',
    'suse': 'zypper',
    'fedora': 'dnf',
    'gentoo': 'equo'
    }

path = getcwd()
env_log_name = 'environment.log'
test_log_name = 'test.log'

def log_cap(log, title, filler='_', major_cap=False):
    if major_cap:
        log(filler*60)
    log(title.center(60, filler))
