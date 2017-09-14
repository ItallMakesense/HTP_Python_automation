"""
Pytest configuration file. Defines custom command lines options, used in test
"""

import pytest

from config import *


def pytest_addoption(parser):
    """
    Official docs:

    register a command line option.

    After command line parsing options are available on the pytest config
    object via ``config.option.NAME`` where ``NAME`` is usually set
    by passing a ``dest`` attribute, for example
    ``addoption("--long", dest="NAME", ...)``.
    """
    parser.addoption(LOC_PASS_OP, action="store")
    parser.addoption(REM_PASS_OP, action="store")
    parser.addoption(LOC_DIR_OP, action="store", default=CLIENT_TEST_DIR)
    parser.addoption(REM_DIR_OP, action="store", default=SERVER_TEST_DIR)
    parser.addoption(TEST_FILE_OP, action="store", default=TEST_FILE)
    parser.addoption(TEST_USER_OP, action="store", default=TEST_USER)
