""" Description """

import logging
import pytest

from config import *
import common
from .base_suite import AccessSuite


DEBUG_LOG = logging.getLogger(DEBUG_LOG)
LOG, LOG_FILE = common.initiate_logger('test_ro_access.log')
TEST_FILE = 'test_read'
EXPORTS_OPTIONS = ['ro', 'sync', 'no_root_squash', 'no_subtree_check']

class TestReadOnly(AccessSuite):
    """ Description """

    @classmethod
    def setup_class(cls):
        LOG.info(common.MAKE_CAP("NFS test - `read only` access"))
        LOG.info(common.MAKE_CAP("%s setup" % cls.__name__))
        #
        cls.log = LOG
        cls.ex_opts = EXPORTS_OPTIONS
        cls.test_file = TEST_FILE
        cls.error_meaning = "Test passed"
        cls.success_meaning = "Test failed"
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        LOG.info(common.MAKE_CAP("%s teardown" % cls.__name__))
        #
        super().teardown_class()
