""" Description """

from subprocess import PIPE
import logging
import pytest

from config import *
import common
from .base_suite import Suite


DEBUG_LOG = logging.getLogger(DEBUG_LOG)
LOG, LOG_FILE = common.initiate_logger('test_owner.log')
TEST_USER = 'test_user'
TEST_FILE = 'test_write'
EXPORTS_OPTIONS = ['rw', 'sync', 'anonuid=%s' % CLIENT_UID,
                   'anongid=%s' % CLIENT_GID, 'no_subtree_check']

class TestOwner(Suite):
    """ Description """

    @classmethod
    def setup_class(cls):
        """ Description """
        LOG.info(common.MAKE_CAP("NFS test - various users access"))
        LOG.info(common.MAKE_CAP("%s setup" % cls.__name__))
        #
        cls.log = LOG
        cls.ex_opts = EXPORTS_OPTIONS
        cls.test_file = os.path.join(SERVER_TEST_DIR, TEST_FILE)
        #
        add = common.execute(['sudo', '-S', 'useradd', TEST_USER],
                            stdin=PIPE, stderr=PIPE, stdout=PIPE,
                            input_line=cls.client_password)
        if not add[2]: # Exit code
            LOG.info("Created - %s" % TEST_USER)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], add)
        #
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        """ Description """
        LOG.info(common.MAKE_CAP("%s teardown" % cls.__name__))
        #
        add = common.execute(['sudo', '-S', 'userdel', TEST_USER],
                            stdin=PIPE, stderr=PIPE, stdout=PIPE,
                            input_line=cls.client_password)
        if not add[2]: # Exit code
            LOG.info("Removed - %s" % TEST_USER)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], add)
        #
        super().teardown_class()

    def test_existing_user(self):
        """ Description """
        cls = self.__class__
        cls.log.info("Existing user access test".center(80, '.'))
        #
        client_test_file = os.path.join(CLIENT_TEST_DIR, cls.test_file)
        try:
            open(client_test_file, 'w').close()
            cls.log.info("Access %s - %s" % (True, client_test_file))
            cls.log.info("Test passed")
        except:
            cls.log.info("Access %s - %s" % (False, client_test_file))
            cls.log.info("Test failed")
            assert False


    def test_new_user(self):
        """ Description """
        cls = self.__class__
        cls.log.info("New user access test".center(80, '.'))
        #
        client_test_file = os.path.join(CLIENT_TEST_DIR, cls.test_file)
        access = common.execute('sudo -S runuser -l {user} -c \"> {file}\"'.format(
                                user=TEST_USER, file=client_test_file), shell=True,
                                stdin=PIPE, stderr=PIPE, stdout=PIPE,
                                input_line=cls.client_password)
        granted = bool(not access[2]) # Based on the exit code
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], access)
        cls.log.info("Access %s - %s" % (granted, client_test_file))
        cls.log.info("Test passed" if not granted else "Test failed")
        assert not granted, "%s access %s" %(TEST_USER, granted)
