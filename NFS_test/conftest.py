"""
Description
"""

import pytest

from config import CLIENT_PASS, SERVER_PASS


def pytest_addoption(parser):
    """ Description """
    parser.addoption(CLIENT_PASS, action="store")
    parser.addoption(SERVER_PASS, action="store")
