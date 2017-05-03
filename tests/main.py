import unittest
import platform
import os
import sys
import logging
import subprocess


if platform.system() != 'Linux':
    sys.exit('Your system is not Linux. Test aborted.')

path = os.getcwd()

env_log = logging.getLogger("enviro_log")
env_log.setLevel(logging.INFO)
env_log_file = logging.FileHandler(path + '/enviro.log')
env_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
env_log_file.setFormatter(env_formatter)
env_log.addHandler(env_log_file)

tests_log = logging.getLogger("tests_log")
tests_log.setLevel(logging.INFO)
tests_log_file = logging.FileHandler(path + '/tests.log')
tests_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
tests_log_file.setFormatter(tests_formatter)
tests_log.addHandler(tests_log_file)

if "paramiko" not in sys.modules:
    env_log.info("       Server command execution:$ pip install paramiko")
    exit_code = subprocess.call("pip install paramiko", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    env_log.info("\"paramiko\" module successfully installed." if not exit_code else "\"paramiko\" module not installed.")

import enviro

env_log.info("________________________________________________________")
env_log.info("___________________Server information___________________")
env_log.info("sysname: {}".format(os.uname().sysname))
env_log.info("nodename: {}".format(os.uname().nodename))
env_log.info("release: {}".format(os.uname().release))
env_log.info("version: {}".format(os.uname().version))
env_log.info("machine: {}".format(os.uname().machine))
env_log.info("python: {}".format(platform.python_version()))
for num, mod in enumerate(sys.modules.keys()):
    if num == 0:
        modules_row = []
    modules_row.append(mod)
    if not num % 4 or num == len(sys.modules.keys()):
        if num == 4:
            env_log.info("modules: {}".format(", ".join(modules_row)))
        else:
            env_log.info("         {}".format(", ".join(modules_row)))
        modules_row = []

# Make Client information here

env_log.info("________________________________________________________")
env_log.info("________________Server preparation began________________")
enviro.server_nfs(enviro.nfs_setup_commands)
env_log.info("________________________________________________________")
env_log.info("________________Client Preparation began________________")
enviro.client_nfs(enviro.nfs_remote_commands)

loader = unittest.defaultTestLoader
suite = loader.discover(path, pattern='*Test.py')
# test_names = ['roTest', 'rwTest', 'ownTest']
# suite = unittest.TestSuite()
# for test in test_names:
#     tests_log.info("{} loading...".format(test))
#     testCase = loader.loadTestsFromModule(__import__(test))
#     tests_log.info("{} loaded.".format(test))
#     suite.addTest(testCase)
#     tests_log.info("{} added to the test suite.".format(test))

env_log.info("________________________________________________________")
env_log.info("_________________Tests execution began__________________")
tests_log.info("_________________Tests execution began__________________")

unittest.TextTestRunner(verbosity=2).run(suite)

env_log.info("________________________________________________________")
env_log.info("______________Client state rollback began_______________")
enviro.client_nfs(enviro.end_remote_commands)
env_log.info("________________________________________________________")
env_log.info("______________Server state rollback began_______________")
enviro.server_nfs(enviro.end_nfs_commands)

if __name__ == "__main__":
    pass
