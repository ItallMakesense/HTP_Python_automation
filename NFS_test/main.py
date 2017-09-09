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


if __name__ == "__main__":
    # command line arguments extraction
    parser = argparse.ArgumentParser(description='Test Suite for NFS file syslem')
    parser.add_argument('--client_pass', default=CLIENT_HOST_PASSWORD, nargs='?',
                        help='Local host password (may be defined in config.py)')
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### ! argument for server password --> give through cmd line

    parser.add_argument('-k', default=None, nargs='?',
                        help='Pytest keyword expressions usage')
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### ! argument for specific test --> join with TESTS_DIR

    args = parser.parse_args()

    # finding password
    CLIENT_HOST_PASSWORD = args.client_pass if args.client_pass else\
                           input('Enter local host password: ')

    # Logger initialising
    INFO_LOG, INFO_FILE = common.initiate_logger(INFO_LOG)
    DEBUG_LOG, DEBUG_FILE = common.initiate_logger(DEBUG_LOG)

    # virtualenv installation
    common.write_to([INFO_LOG.info, DEBUG_LOG.info], common.MAKE_CAP("Environment installation"))
    try:
        setup_venv(DEBUG_LOG)
        INFO_LOG.info("Installed - %s" % ENV_DIR)
    except Exception as error:
        DEBUG_LOG.error(error)

    # combining pytest commands
    keywords = ['-k', args.k] if args.k else ['']
    PYTEST_LINE = ['-m', 'pytest', '-s', *keywords, TESTS_DIR]

    # test execution in a subprocess
    common.write_to([INFO_LOG.info, DEBUG_LOG.info], common.MAKE_CAP("Testing start"))
    DEBUG_FILE.close()
    result = common.execute(['sudo', '-S', PYTHON_PATH, *PYTEST_LINE],
                            stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE,
                            input_line=CLIENT_HOST_PASSWORD)
    common.write_to([INFO_LOG.info, DEBUG_LOG.error], result)
    common.write_to([INFO_LOG.info, DEBUG_LOG.info], common.MAKE_CAP("Testing end"))

    # removing virtualenv
    common.write_to([INFO_LOG.info, DEBUG_LOG.info], common.MAKE_CAP("Environment removing"))
    try:
        tear_down.remove_dir(ENV_DIR)
        INFO_LOG.info("Removed - %s" % ENV_DIR)
    except OSError as error:
        DEBUG_LOG.error(error)
