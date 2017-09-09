""" Description """

import logging
import pytest

from config import *
import common
from .base_suite import Suite


DEBUG_LOG = logging.getLogger(DEBUG_LOG)
LOG, LOG_FILE = common.initiate_logger('test_owner.log')
TEST_USER = 'test_user'
TEST_FILE = 'test_write'
EXPORTS_OPTIONS = ['rw', 'sync', 'no_root_squash', 'no_subtree_check']

class TestOwner(Suite):
    """ Description """

    @classmethod
    def setup_class(cls):
        """ Description """
        LOG.info(common.MAKE_CAP("NFS test - various users access"))
        LOG.info(common.MAKE_CAP("%s setup" % cls.__name__))
        cls.log = LOG
        cls.ex_opts = EXPORTS_OPTIONS
        cls.test_file = os.path.join(SERVER_TEST_DIR, TEST_FILE)
        add = common.execute(['sudo', '-S', 'useradd', TEST_USER],
                            stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE,
                            input_line=CLIENT_HOST_PASSWORD)
        if not add[2]: # Exit code
            LOG.info("Created - %s" % TEST_USER)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], add)
        super().setup_class()
    
    @classmethod
    def teardown_class(cls):
        """ Description """
        cls.log.info(common.MAKE_CAP("%s teardown" % cls.__name__))
        add = common.execute(['sudo', '-S', 'userdel', TEST_USER],
                            stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE,
                            input_line=CLIENT_HOST_PASSWORD)
        if not add[2]: # Exit code
            LOG.info("Removed - %s" % TEST_USER)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], add)
        super().setup_class()
    
    def test_existing_user(self, method):
        """ Description """
        cls = self.__class__
        #
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Existing user access test start"))
        try:
            open(new_file_path, 'w').close()
            cls.log.info("Created - %s" % new_file_path)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not Created - %s" % new_file_path)
            cls.log.info(cls.error_meaning)
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Creation test end"))



    def test_new_user(self, method):
        """ Description """
        cls = self.__class__
        #
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Creation test start"))
        try:
            open(new_file_path, 'w').close()
            cls.log.info("Created - %s" % new_file_path)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not Created - %s" % new_file_path)
            cls.log.info(cls.error_meaning)
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Creation test end"))
