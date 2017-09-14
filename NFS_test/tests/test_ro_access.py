"""
Module keeps test suite for checking nfs client's `read-only` access permission.

To change the class' attributes, defined through command line arguments
(for example, nfs server test file) directly in this module
(not with `config.py` or through those command line arguments), simply redefine
them in the class body
"""

import pytest

from config import *
import common
from .base_suite import AccessSuite


LOG = common.initiate_logger(RO_TEST_LOG)


class TestReadOnly(AccessSuite):
    """
    Test case for checking nfs client's `read-only` access permission
    for the mounted test folder from nfs server
    """

    @classmethod
    def setup_class(cls):
        """
        Run `base_suite.AccessSuite.setup_class` with this test case arguments.
        Argument `expect_fail` is `True` due to expected access denying
        """
        super().setup_class(LOG, RO_EXPORTS, "NFS test - `read only` access",
                            expect_fail=True)
