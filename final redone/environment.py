"""
This module is designed to keep all the utils, that dealing with system
environment, both server's and client's, allowing tests to start and complete
"""

from sub import *
import logging
import paramiko
import subprocess
import sys


log = logging.getLogger(env_log_name)


def ssh_connect(function):

    """ This decorator allows to execute wrapped function on a remote
        machine, and return the execution result, if it is provided """

    def wrapper(*args):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=client_username, hostname=client_address,\
                    password=client_password)
        log_cap(log.debug, "SSH {user}@{ip} connection opened".format(\
                               user=client_username, ip=client_address),\
                               filler='\\')
        done = function(*args, ssh=ssh)
        ssh.close()
        log_cap(log.debug, "SSH {user}@{ip} connection closed".format(\
                               user=client_username, ip=client_address),\
                               filler='/')
        return done
    return wrapper


@ssh_connect
def get_distribution(ssh='connect'):

    """ This function used to receive linux distribution name
        of the remote machine through ssh connection, provided by
        ssh_connect decorator """

    command = "python -c \"from platform import linux_distribution; " +\
              "print(linux_distribution(full_distribution_name=0)[0])\""
    log.info("Client command execution:$ %s" % command)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode().strip().lower()


def filter_for(this_log, string):

    """ This function fiters empty lines in given raw line,
        and logs the rest to the given log, line by line """

    for line in string.split("\n"):
        if line:
            this_log(line)


def server_execute(command):

    """ This function executes given command as superuser in the
        server's shell and returns the result, including errors (if any) """

    pipe = subprocess.PIPE
    p = subprocess.Popen("sudo -S %s" % command, shell=True,\
                            stdin=pipe, stdout=pipe, stderr=pipe)
    log.info("Server command execution:$ %s" % command)
    result, errors = p.communicate(input=(server_password+'\n').encode())
    result = result.decode()
    errors = errors.decode().lstrip(\
               "[sudo] password for %s: " % client_username)
    filter_for(log.debug, result)
    filter_for(log.error, errors)
    return result, errors


@ssh_connect
def client_execute(command, ssh='connect'):

    """ This function executes given command as superuser in the
        client's shell (through ssh_connect decorator) and returns
        the result, including errors (if any) """

    log.info("Client command execution:$ %s" % command)
    stdin, stdout, stderr = ssh.exec_command("sudo -S %s" % command)
    stdin.write((client_password + '\n').encode())
    stdin.flush()
    result = stdout.read().decode()
    errors = stderr.read().decode().lstrip("[sudo] password for %s: "\
                                            % client_username)
    filter_for(log.debug, result)
    filter_for(log.error, errors)
    return result, errors


def execute_all(commands, executor):

    """ Simple function for executing commands, one by one, by the given
        executor function. Catches exceptions during execution """

    for command in commands:
        try:
            executor(command)
        except:
            sys.exit("Errors occured. Check logs for more info")


client_linux = get_distribution()

steps = {
    'setup': [
        "{pm} install nfs-kernel-server nfs-common -y".format(\
        pm=packages[linux]),
        "mkdir -p {home}/test_nfs {home}/test_ro_nfs".format(home=home_path),
        "bash -c '> {home}/test_nfs/edition_check'".format(home=home_path),
        "bash -c '> {home}/test_ro_nfs/edition_check'".format(home=home_path),
        "bash -c \"echo \'{line}\' >> /etc/exports\"".format(\
        line="{home}/test_nfs {ip}(rw,sync,no_root_squash)"\
        .format(home=home_path, ip=client_address)),
        "bash -c \"echo \'{line}\' >> /etc/exports\"".format(\
        line="{home}/test_ro_nfs {ip}(ro,sync)".format(\
        home=home_path, ip=client_address)),
        "exportfs -a",
        "service nfs-kernel-server restart"
        ],

    'remote_setup': [
        "{pm} install nfs-kernel-server nfs-common -y".format(\
        pm=packages[client_linux]),
        "service nfs-kernel-server start",
        "mkdir -p /mnt/test_nfs /mnt/test_ro_nfs",
        "mount {ip}:{home}/test_nfs /mnt/test_nfs".format(\
        ip=server_address, home=home_path),
        "mount {ip}:{home}/test_ro_nfs /mnt/test_ro_nfs".format(\
        ip=server_address, home=home_path)
        ],

    'remote_remove': [
        "umount /mnt/test_ro_nfs",
        "umount /mnt/test_nfs",
        "rm -r /mnt/test_ro_nfs /mnt/test_nfs",
        "service nfs-kernel-server stop",
        "{pm} remove nfs-kernel-server nfs-common -y".format(\
        pm=packages[client_linux])
        ],

    'remove': [
        "service nfs-kernel-server stop",
        "sed -i '$ d' /etc/exports",
        "sed -i '$ d' /etc/exports",
        "rm -r {home}/test_nfs {home}/test_ro_nfs".format(\
        home=home_path),
        "{pm} remove nfs-kernel-server nfs-common -y".format(\
        pm=packages[linux])
        ]
    }
