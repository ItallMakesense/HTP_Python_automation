#!/bin/sh

"""
(Supposed to work in a pair with Lnx52.sh, started on a separate computer)

Script that every 3 minutes adds a random string with a length
of 10 symbols to $HOME/sync/random_string.log.

If the last random string ends with even digit, the script prints out “EVEN!”
and the number itself to the current console; if it is odd or a letter,
the script prints “ODD!” and the number itself.

Steps:
 1. Synchronize two computers via ssh.
 2. Create sync directory:$ sudo mkdir ~/sync
"""


while true
do
date +%T | tr -d '\n' >> $HOME/sync/random_string.log
string=$(head /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 10)
echo -n $string >> $HOME/sync/random_string.log
echo >> $HOME/sync/random_string.log
string_S=$(echo -n $string | tail -c 1)
if [[ "$string_S" -ne 'a-zA-Z' ]]
then
num=$(expr $string_S % 2)
if [[ $num -eq 0 ]]
then echo "EVEN!"; echo $string_S
elif [[ $num -ne 0 ]]
then echo "ODD!"; echo $string_S
fi
elif [[ "$string_S" -eq 'a-zA-Z' ]]
then echo "ODD!"; echo $string_S
fi
sleep 180
done

# A 'date' command with '%T' option makes .log input to start with current time.
# Further is just deleting of new line symbol at the end of 'date' output.
# A 'string' variable contains commands making random string with 10 symbols
# (first 10 lines of randomly generated file sorting by 'tr' command,
# which passes only needed symbols, and in the end cuts all to 10 symbols).
# Next is just appending of this line to .log (echo \n ...; echo ...).
# A 'string_S' variable contains the last symbol of $string var (simply by "tailing" the last symbol).
# All that remains in code - is our conditions...
# Except 'sleep' - after that it's just waits for 3 minutes :)

# This script can be terminated by a command "bash Lnx51.sh"
# (it will work till "ctrl+c" or closing terminal if OS is ubuntu)

# Either it can be placed in the background as daemon:
# use the command "bash Lnx51.sh &"

# Even more - it can start everytime the terminal opens:
# use the command "echo >> ~/.bashrc; echo 'bash ~/Lnx51.sh &' >> ~/.bashrc"


