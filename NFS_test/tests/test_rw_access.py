""" Description """

import logging
import pytest

from config import *
import common
from .base_suite import AccessSuite


DEBUG_LOG = logging.getLogger(DEBUG_LOG)
LOG, LOG_FILE = common.initiate_logger('test_rw_access.log')
TEST_FILE = 'test_write'
EXPORTS_OPTIONS = ['rw', 'sync', 'no_root_squash', 'no_subtree_check']

class TestReadWrite(AccessSuite):
    """ Description """

    @classmethod
    def setup_class(cls):
        LOG.info(common.MAKE_CAP("NFS test - `read and write` access"))
        LOG.info(common.MAKE_CAP("%s setup" % cls.__name__))
        cls.log = LOG
        cls.ex_opts = EXPORTS_OPTIONS
        cls.test_file = os.path.join(SERVER_TEST_DIR, TEST_FILE)
        cls.error_meaning = "Test failed"
        cls.success_meaning = "Test passed"
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        cls.log.info(common.MAKE_CAP("%s teardown" % cls.__name__))
        super().teardown_class()
