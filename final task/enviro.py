import subprocess
import platform
import os.path
import sys
import logging
import paramiko


env_log = logging.getLogger("enviro_log")
env_log_o = logging.getLogger("enviro_log.stdout")
env_log_e = logging.getLogger("enviro_log.stderr")

server_address = '192.168.56.1'
server_password = 'me'
client_username = 'virtual'
client_address = '192.168.56.5'
client_password = 'me'
home_path = os.path.expanduser('~')
linux_distribution = platform.linux_distribution(full_distribution_name=0)[0]


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

def client_connect(function):
    def wrapper(*args):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=client_username, hostname=client_address, password=client_password)
        env_log.info("_______SSH {}@{} connection opened_______".format(client_username, client_address))
        done = function(*args, ssh=ssh)
        ssh.close()
        env_log.info("_______SSH {}@{} connection closed_______".format(client_username, client_address))
        return done
    return wrapper

# def pretty_log_line(log, item):
#     if '\n' in item:
#         for line in item.split('\n'):
#             pretty_log_line(log, line)
#     else:
#         log(item)

def sudo_command_executor(command):
    can = subprocess.PIPE
    proc = subprocess.Popen("sudo -S {}".format(command), shell=True, stdin=can, stdout=can, stderr=can)
    outs, errors = proc.communicate(input="{}\n".format(server_password).encode())
    env_log.info("       Server command execution:$ {}".format(command))
    # pretty_log_line(env_log_o.info, outs.decode())
    # pretty_log_line(env_log_e.info, errors.decode())
    for outline in outs.decode().split("\n"):
        if outline:
            env_log_o.info(outline)
    for errorline in errors.decode().lstrip("[sudo] password for {}: ".format(client_username)).split("\n"):
        if errorline:
            env_log_e.info(errorline)

def server_nfs(commands):
    for command in commands:
        try:
            sudo_command_executor(command)
        except:
            sys.exit("Errors occured. Check logs for more info.")

@client_connect
def get_remote_distribution(ssh='connect'):
    command = "python -c \"import platform; print(platform.linux_distribution(full_distribution_name=0)[0])\""
    env_log.info("       Client command execution:$ {}".format(command))
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    return result

@client_connect
def client_nfs(commands, ssh='connect'):
    for command in commands:
        try:
            stdin, stdout, stderr = ssh.exec_command("sudo -S {}".format(command))
            stdin.write("{}\n".format(client_password).encode())
            stdin.flush()
            env_log.info("       Client command execution:$ {}".format(command))
            for outline in stdout.read().decode().split("\n"):
                if outline:
                    env_log_o.info(outline)
            for errorline in stderr.read().decode().lstrip("[sudo] password for {}: ".format(client_username)).split("\n"):
                if errorline:
                    env_log_e.info(errorline)
        except:
            sys.exit("Errors occured. Check logs for more info.")

@client_connect
def executor(command, ssh='connect'):
    stdin, stdout, stderr = ssh.exec_command("sudo -S {}".format(command))
    stdin.write("{}\n".format(client_password).encode())
    stdin.flush()
    env_log.info("       Client command execution:$ {}".format(command))
    outs = stdout.read().decode()
    errors = stderr.read().decode().lstrip("[sudo] password for {}: ".format(client_username))
    for outline in outs.split("\n"):
        if outline:
            env_log_o.info(outline)
    for errorline in errors.split("\n"):
        if errorline:
            env_log_e.info(errorline)
    return errors

client_linux_distribution = get_remote_distribution()

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
                        "service nfs-kernel-server restart"]

nfs_remote_commands = [ "{} install nfs-kernel-server nfs-common -y".format(package_explore(client_linux_distribution)),
                        "service nfs-kernel-server start",
                        "mkdir -p /mnt/test_nfs /mnt/test_ro_nfs",
                        "mount {}:{}/test_nfs /mnt/test_nfs".format(server_address, home_path),
                        "mount {}:{}/test_ro_nfs /mnt/test_ro_nfs".format(server_address, home_path)]

end_remote_commands = [ "umount /mnt/test_ro_nfs",
                        "umount /mnt/test_nfs",
                        "rm -r /mnt/test_ro_nfs /mnt/test_nfs",
                        "service nfs-kernel-server stop",
                        "{} remove nfs-kernel-server nfs-common -y".format(package_explore(client_linux_distribution))]

end_nfs_commands =    [ "service nfs-kernel-server stop",
                        "sed -i '$ d' /etc/exports",
                        "sed -i '$ d' /etc/exports",
                        "rm -r {}/test_nfs {}/test_ro_nfs".format(home_path, home_path),
                        "{} remove nfs-kernel-server nfs-common -y".format(package_explore(linux_distribution))]
