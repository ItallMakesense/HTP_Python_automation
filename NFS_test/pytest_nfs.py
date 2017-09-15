"""
The starting module of this package. In fact it's a wrapper for the pytest
normal test execution. Works with python 2.7+ versions.

Responsible for:
    - Ensuring, that local and remote host's passwords were entered
      in any way: through `config.py` or command line. And if they weren't, asks
      to enter them
    - Installation of virtual environment before the test execution
    - Test execution itself, besides in subprocess, and with sudo privilegues
    - Removing of virtual environment after testing was ended

All the necessary information is writing to logs.

This module can be run with custom command line arguments,
written in `config.py`, and with arguments of `Pytest` package itself -
all of it will be transferred to the subprocess.
Examples (using default options of `config.py`):

    python pytest_nfs.py --client_pass=one --server_pass=another

    python pytest_nfs.py tests/test_owner.py -k=test_new_user

    python pytest_nfs.py --ignore=test_owner.py
"""

from sys import version_info
import argparse

from config import *
import common


def setup_venv():
    """
    Installs python virtual environment, with `Fabric` and `Pytest` packages.
    Requires `pip` package manager
    """
    setup_order = [
        [SHELL_PIP, 'install', 'virtualenv'],
        ['virtualenv', ENV_DIR],
        [ENV_PIP, 'install', 'fabric3', 'pytest']
    ]
    for step in setup_order:
        common.execute(step, collect=True)


def get_passwd(line):
    """ Asks for password to enter. Not ends, untill something is entered """
    passwd = ''
    ver_input = input if version_info.major == 3 else raw_input
    while not passwd:
        passwd = ver_input(line)
    return passwd


if __name__ == "__main__":
    # command line arguments extraction
    parser = argparse.ArgumentParser(
        description='Test suite for NFS file syslem')
    parser.add_argument(LOC_PASS_OP, default=CLIENT_HOST_PASSWORD, nargs='?',
                        help='Local host password (may be defined in config.py)',
                        metavar='password')
    parser.add_argument(REM_PASS_OP, default=SERVER_HOST_PASSWORD, nargs='?',
                        help='Local host password (may be defined in config.py)',
                        metavar='password')
    args, pytest_options = parser.parse_known_args()

    # finding passwords
    client_password = args.client_pass if args.client_pass else\
        get_passwd('Enter local host password: ')
    server_password = args.server_pass if args.server_pass else\
        get_passwd('Enter remote host password: ')

    # Logger initialising
    INFO_LOG = common.initiate_logger(INFO_LOG)
    DEBUG_LOG, DEBUG_FILE = common.initiate_logger(DEBUG_LOG, with_file=True)
    CMD_LOG, CMD_FILE = common.initiate_logger(LOC_CMD_LOG, with_file=True)

    # virtualenv installation
    common.write_to([INFO_LOG.info, DEBUG_LOG.info],
                    common.MAKE_CAP("Environment installation"))
    try:
        setup_venv()
        INFO_LOG.info("Installed - %s" % ENV_DIR)
    except Exception as error:
        DEBUG_LOG.error(error)
        exit()

    # combining pytest commands
    pass_line = [LOC_PASS_OP, client_password, REM_PASS_OP, server_password]
    pytest_line = ['-m', 'pytest', '-s'] + pytest_options + pass_line

    # test execution in a subprocess
    common.write_to([INFO_LOG.info, DEBUG_LOG.info],
                    common.MAKE_CAP("Testing"))
    DEBUG_FILE.close()
    CMD_FILE.close()
    end = common.execute(['sudo', '-S', ENV_PYTHON] + pytest_line,
                                    input_line=client_password, collect=True,
                                    pytest=True, secure=[client_password,
                                                         server_password])
    common.write_to([INFO_LOG.info, DEBUG_LOG.error], [end[0], end[1]])

    # removing virtualenv
    common.write_to([INFO_LOG.info, DEBUG_LOG.info],
                    common.MAKE_CAP("Environment removing"))
    try:
        common.execute(['rm', '-r', ENV_DIR], collect=True, pytest=True)
        common.write_to([INFO_LOG.info, DEBUG_LOG.debug],
                        "Removed - %s" % ENV_DIR)
    except OSError as error:
        DEBUG_LOG.error(error)
