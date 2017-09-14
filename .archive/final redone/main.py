"""
Main executive module
"""

from sub import *
import subprocess
import unittest
import logging
import os
import sys

# Program is designed for linux systems. If it's started on another
# systems, the program stops
if not sys.platform.startswith('linux'):
    sys.exit('Your system is not Linux. Test aborted')

# Setting environment logger
env_log = logging.getLogger(env_log_name)
env_log.setLevel(logging.DEBUG)
env_log_file = logging.FileHandler(os.path.join(path, env_log_name))
env_log_file.setFormatter(logging.Formatter(\
             "%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
env_log.addHandler(env_log_file)

# Setting test logger
test_log = logging.getLogger(test_log_name)
test_log.setLevel(logging.DEBUG)
test_log_file = logging.FileHandler(os.path.join(path, test_log_name))
test_log_file.setFormatter(logging.Formatter(\
              "%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
test_log.addHandler(test_log_file)

# Checking, if paramiko is installed (and install it, if not).
# Paramiko module is essential
if "paramiko" not in sys.modules:
    env_log.info("Server command execution:$ pip install paramiko")
    exit_code = subprocess.call("pip install paramiko", shell=True,\
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    env_log.info("\"paramiko\" module successfully installed." if not exit_code\
                    else "\"paramiko\" module not installed.")

# Providing server information, writing it to environment log
log_cap(env_log.info, "Server information")
env_log.info("sysname: %s" % os.uname()[0])
env_log.info("nodename: %s" % os.uname()[1])
env_log.info("release: %s" % os.uname()[2])
env_log.info("version: %s" % os.uname()[3])
env_log.info("machine: %s" % os.uname()[4])
env_log.info("python: %s" % ".".join(map(str, sys.version_info)))
env_log.info("modules: %s" % ", ".join(sys.modules.keys()))


from environment import execute_all, server_execute, client_execute, steps

# Preparing server system environment
log_cap(env_log.info, "Server preparation began", filler='=', major_cap=True)
execute_all(steps['setup'], server_execute)

# Preparing client system environment
log_cap(env_log.info, "Client preparation began", filler='=', major_cap=True)
execute_all(steps['remote_setup'], client_execute)

# Creating test suite and executing tests within it
loader = unittest.defaultTestLoader
suite = loader.discover(path, pattern='test*')
log_cap(env_log.info, "Tests execution began", filler='=', major_cap=True)
log_cap(test_log.info, "Tests execution began", filler='=', major_cap=True)
unittest.TextTestRunner(verbosity=2).run(suite)
log_cap(test_log.info, "Tests execution began", filler='=')
log_cap(env_log.info, "Tests execution began", filler='=')

# Returning client system condition to it's previous state
log_cap(env_log.info, "Client state rollback began", filler='=', major_cap=True)
execute_all(steps['remote_remove'], client_execute)

# Returning server system condition to it's previous state
log_cap(env_log.info, "Server state rollback began", filler='=', major_cap=True)
execute_all(steps['remove'], server_execute)
