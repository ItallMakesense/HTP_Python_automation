"""
Module keeps test suite for checking nfs client's `read and write` access
permission.

To change the class' attributes, defined through command line arguments
(for example, nfs server test file) directly in this module
(not with `config.py` or through those command line arguments), simply redefine
them in the class body
"""

import pytest

from config import *
import common
from .base_suite import AccessSuite


LOG = common.initiate_logger(RW_TEST_LOG)


class TestReadWrite(AccessSuite):
    """
    Test case for checking nfs client's `read and write` access permission
    for the mounted test folder from nfs server
    """

    @classmethod
    def setup_class(cls):
        """
        Run `base_suite.AccessSuite.setup_class` with this test case arguments
        """
        super().setup_class(LOG, RW_EXPORTS, "NFS test - `read and write` access")
