import subprocess
import platform
import os.path
import paramiko
import sys
import logging
import time


def client_connect(function):
    def wrapper(*args):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=client_username, hostname=client_address, password=client_password)
        done = function(*args, ssh=ssh)
        ssh.close()
        return done
    return wrapper

def package_explore(linux_distribution):
    package_manager = None
    if linux_distribution.strip().lower() in ['debian', 'ubuntu']:
        package_manager = 'apt-get'
    elif linux_distribution.strip().lower() in ['fedora']:
        package_manager = 'dnf'
    elif linux_distribution.strip().lower() in ['gentoo']:
        package_manager = 'equo'
    elif linux_distribution.strip().lower() in ['yellowdog', 'redhat', 'centos']:
        package_manager = 'yum'
    elif linux_distribution.strip().lower() in ['suse']:
        package_manager = 'zypper'
    return package_manager

@client_connect
def get_remote_distribution(ssh='connect'):
    stdin, stdout, stderr = ssh.exec_command("python -c \"import platform; print(platform.linux_distribution(full_distribution_name=0)[0])\"")
    result = stdout.read().decode()
    return result

def sudo_command_executor(command, log_file):
    can = subprocess.PIPE
    proc = subprocess.Popen("sudo -S {}".format(command), shell=True, stdin=can, stdout=can, stderr=can)
    outs, errors = proc.communicate(input="{}\n".format(server_password).encode())
    log_file.write('\n{}: server \"{}\" result:\n{}'.format(time.ctime(), command, outs.decode()))
    log_file.write('\n{}: server \"{}\" errors:\n{}'.format(time.ctime(), command, errors.decode()))


def server_nfs(commands, log_file):
    for command in commands:
        try:
            sudo_command_executor(command, log_file)
            log_file.write('\n')
        except:
            sys.exit("Errors occured. Check logs for more info.")

@client_connect
def client_nfs(commands, log_file, ssh='connect'):
    for command in commands:
        try:
            stdin, stdout, stderr = ssh.exec_command("sudo -S {}".format(command))
            stdin.write("{}\n".format(client_password).encode())
            stdin.flush()
            log_file.write('\n{}: client \"{}\" result:\n{}'.format(time.ctime(), command, stdout.read().decode()))
            log_file.write('\n{}: client \"{}\" errors:\n{}'.format(time.ctime(), command, stderr.read().decode()))
        except:
            sys.exit("Errors occured. Check logs for more info.")

server_address = '192.168.56.1'
server_password = 'me'
client_username = 'virtual'
client_address = '192.168.56.5'
client_password = 'Me'
home_path = os.path.expanduser('~')

linux_distribution = platform.linux_distribution(full_distribution_name=0)[0]

nfs_setup_commands =  [ "{} install nfs-kernel-server nfs-common -y".format(package_explore(linux_distribution)),
                        "mkdir -p {}/test_nfs {}/test_ro_nfs".format(home_path, home_path),
                        "bash -c '> {}/test_nfs/edition_check'".format(home_path),
                        "bash -c '> {}/test_ro_nfs/edition_check'".format(home_path),
                        "bash -c \"echo \'{}\' >> /etc/exports\"".format\
                        ("{}/test_nfs {}(rw,sync,no_root_squash,no_subtree_check)".format\
                        (home_path, client_address)),
                        "bash -c \"echo \'{}\' >> /etc/exports\"".format\
                        ("{}/test_ro_nfs {}(ro,sync,no_subtree_check)".format\
                        (home_path, client_address)),
                        "exportfs -a",
                        "service nfs-kernel-server restart"
                      ]
nfs_remote_commands = [ "{} install nfs-kernel-server nfs-common -y".format(package_explore(get_remote_distribution())),
                        "service nfs-kernel-server start",
                        "mkdir -p /mnt/test_nfs /mnt/test_ro_nfs",
                        "mount {}:{}/test_nfs /mnt/test_nfs".format(server_address, home_path),
                        "mount {}:{}/test_ro_nfs /mnt/test_ro_nfs".format(server_address, home_path)
                      ]
end_remote_commands = [ "umount /mnt/test_ro_nfs",
                        "umount /mnt/test_nfs",
                        "rm -r /mnt/test_ro_nfs /mnt/test_nfs",
                        "service nfs-kernel-server stop",
                        "{} remove nfs-kernel-server nfs-common -y".format(package_explore(get_remote_distribution()))
                      ]
end_nfs_commands =    [ "service nfs-kernel-server stop",
                        "sed -i '$ d' /etc/exports",
                        "sed -i '$ d' /etc/exports",
                        "rm -r {}/test_nfs {}/test_ro_nfs".format(home_path, home_path),
                        "{} remove nfs-kernel-server nfs-common -y".format(package_explore(linux_distribution))
                      ]
