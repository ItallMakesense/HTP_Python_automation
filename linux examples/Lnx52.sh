#!/bin/sh

"""
(Supposed to work in a pair with Lnx52.sh, started on a separate computer)

cript that every 2 minutes scans ssh-connected computer for content
in $HOME/sync directory, and copies all to self $HOME/sync directory.

Steps:
 1. Synchronize two computers via ssh.
 2. Create sync directory:$ sudo mkdir ~/sync
"""

# Change user@ip, using relevant values.

while true
do
scp -r user@ip:~/sync ~/
sleep 120
done

# This script can be terminated by a command "bash Lnx52.sh"
# (it will work till "ctrl+c" or closing terminal if OS is ubuntu)

# Either it can be placed in the background as daemon:
# use the command "bash Lnx52.sh &"

# Even more - it can start everytime the terminal opens:
# use the command "echo >> ~/.bashrc; echo 'bash ~/Lnx52.sh &' >> ~/.bashrc"