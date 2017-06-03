#!/bin/bash

"""
Performs automated installation of Java 8 Runtime Environment (JRE)
and latest Python 2.x from the official web site.

After all installations prints out to the terminal Java and Python
versions and installation results.
"""

kill -9 $(pidof java) 2>/dev/null
kill -9 $(pidof python) 2>/dev/null

rem=$(whereis java)
for dir in $rem
do
rm -rf $dir 2>/dev/null
done

#java
cd /opt/
wget -O jre8.tar.gz --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://javadl.oracle.com/webapps/download/AutoDL?BundleId=211989"
tar xzf jre8.tar.gz

cd /opt/jre1.8.0_101/
alternatives --install /usr/bin/java java /opt/jre1.8.0_101/bin/java 2
echo 3 | alternatives --config java
export PATH=$PATH:/opt/jre1.8.0_101/bin

#python
yum install gcc -y
cd /usr/src
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
tar xzf Python-2.7.13.tgz

cd Python-2.7.13
./configure
make altinstall

java -version; whereis java 2>/dev/null
python --version; whereis python 2>/dev/null