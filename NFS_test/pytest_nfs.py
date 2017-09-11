"""
Description

Minuses:
    - !python3! required on a remote server
"""
import subprocess as sp
import argparse

from config import *
import common
import tear_down


def setup_venv(logger):
    """ Description """
    setup_order = [
        ['pip', 'install', 'virtualenv'],
        ['virtualenv', ENV_DIR],
        [PIP_PATH, 'install', 'fabric3', 'pytest']
        ]
    for step in setup_order:
        result = common.execute(step, stdout=sp.PIPE, stderr=sp.PIPE)
        common.write_to([logger.debug, logger.error], result)

def get_passwd(line):
    """ Description """
    passwd = ''
    while not passwd:
        passwd = input(line)
    return passwd


if __name__ == "__main__":
    # command line arguments extraction
    parser = argparse.ArgumentParser(description='Test suite for NFS file syslem')
    parser.add_argument(CLIENT_PASS, default=CLIENT_HOST_PASSWORD, nargs='?',
                        help='Local host password (may be defined in config.py)')
    parser.add_argument(SERVER_PASS, default=SERVER_HOST_PASSWORD, nargs='?',
                        help='Local host password (may be defined in config.py)')
    parser.add_argument('-k', default=None, nargs='?',
                        help='Pytest keyword expressions usage. Write specific'
                             ' \'test_case\', or \'test_one or test_two\' for'
                             ' a couple of tests, and \'not test_three\''
                             ' to exclude it. Also \'test_case and test_function\''
                             ' can be used to run only one test in case')
    args = parser.parse_args()

    # finding passwords
    client_password = args.client_pass if args.client_pass else\
                           get_passwd('Enter local host password: ')
    server_password = args.server_pass if args.server_pass else\
                           get_passwd('Enter remote host password: ')

    # Logger initialising
    INFO_LOG, INFO_FILE = common.initiate_logger(INFO_LOG)
    DEBUG_LOG, DEBUG_FILE = common.initiate_logger(DEBUG_LOG)

    # virtualenv installation
    common.write_to([INFO_LOG.info, DEBUG_LOG.info],
                    common.MAKE_CAP("Environment installation"))
    try:
        setup_venv(DEBUG_LOG)
        INFO_LOG.info("Installed - %s" % ENV_DIR)
    except Exception as error:
        DEBUG_LOG.error(error)

    # combining pytest commands
    keywords = ['-k', args.k] if args.k else ['']
    pytest_line = ['-m', 'pytest', '-s', *keywords, TESTS_DIR]
    args_line = [CLIENT_PASS, client_password, SERVER_PASS, server_password]
    print(['sudo', '-S', PYTHON_PATH, *pytest_line, *args_line])

    # test execution in a subprocess
    common.write_to([INFO_LOG.info, DEBUG_LOG.info], common.MAKE_CAP("Testing"))
    DEBUG_FILE.close()
    result = common.execute(['sudo', '-S', PYTHON_PATH, *pytest_line, *args_line],
                            stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE,
                            input_line=client_password)
    common.write_to([INFO_LOG.info, DEBUG_LOG.error], result)

    # removing virtualenv
    common.write_to([INFO_LOG.info, DEBUG_LOG.info],
                    common.MAKE_CAP("Environment removing"))
    try:
        tear_down.remove_dir(ENV_DIR)
        INFO_LOG.info("Removed - %s" % ENV_DIR)
    except OSError as error:
        DEBUG_LOG.error(error)
