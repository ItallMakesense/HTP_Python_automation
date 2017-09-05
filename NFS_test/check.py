import fabric
import os
import sys
import subprocess as sp
from platform import dist
from threading import Thread
from time import sleep



print("OS ACCESS TO mnt", os.access('/mnt', os.W_OK))
# print("LOCAL is", LOCAL)
print("GET LOGIN", os.getlogin())
print("SCRIPT ARGS", sys.argv)
print(dist()[0])
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
print(packages[dist()[0].lower()])
try:
    with open('/etc/exports', 'r+') as file:
        print(file.read())
        file.write("Writings\n")
        print(file.read())
except:
    print('NO SUDO')
