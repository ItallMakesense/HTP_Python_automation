#!bin/bash

#Path to logs
path=/tmp/logs
#Ubuntu
date +%T >> $path 2>&1
sudo apache2 -v >> $path 2>&1
if [[ $? -ne 0 ]]
then date +%T >> $path 2>&1
sudo apt install apache2 -y >> $path 2>&1
date +%T >> $path 2>&1
sudo update-rc.d apache2 disable >> $path 2>&1
fi
#CentOS
date +%T >> $path 2>&1
sudo httpd -v >> $path 2>&1
if [[ $? -ne 0 ]]
then date +%T >> $path 2>&1
sudo yum install httpd -y >> $path 2>&1
date +%T >> $path 2>&1
sudo chkconfig httpd off >> $path 2>&1
fi
#Informing about removing
(tac /var/log/apt/history.log 2> /dev/null | \grep remove.apache -C 1 2>/dev/null) || sudo yum history list httpd
#Start-stop
if [[ $2 = 11 ]] || [[ $2 = 12 ]]
then date +%T >> $path 2>&1
service apache2 start >> $path 2>&1 || service httpd start >> $path 2>&1
elif [[ $2 = 21 ]] || [[ $2 = 23 ]]
then date +%T >> $path 2>&1
service apache2 stop >> $path 2>&1 || service httpd stop >> $path 2>&1
fi
#Copying to remote system (mine was root@)
scp /tmp/logs root@$1:/tmp/logs
