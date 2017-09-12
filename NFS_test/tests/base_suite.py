"""
Description
"""

import pytest

from config import *
import common
from bridge import Bridge
import set_up
import tear_down


DEBUG_LOG, DEBUG_FILE = common.initiate_logger(DEBUG_LOG)


class Suite:
    """ Description """

    # Dummy attributes. It must be changed in child test suites
    log, ex_opts, test_file, error_meaning, success_meaning = range(5)

    # Getting paswords from command line
    client_password = pytest.config.getoption('client_pass')
    server_password = pytest.config.getoption('server_pass')

    @classmethod
    def setup_class(cls):
        """ Description """
        cls.bridge = Bridge(cls.server_password)
        # Set up server
        cls.bridge.sudo('mkdir %s' % SERVER_TEST_DIR)
        cls.bridge.send(SERVER_TEST_DIR, set_up)
        rem_res = cls.bridge.remote_shell(cls.bridge.python, SERVER_TEST_DIR,
                                          set_up, cls.ex_opts)
        act = "succeeded" if rem_res.succeeded else "failed"
        cls.log.info("Server setup %s" % act)
        cls.bridge.remove(SERVER_TEST_DIR, only_files=True)
        # Set up client
        loc_res = set_up.Suite.client(CLIENT_TEST_DIR)
        act = "succeeded" if loc_res else "failed"
        cls.log.info("Client setup %s" % act)

    @classmethod
    def teardown_class(cls):
        """ Description """
        # Tear down client
        loc_res = tear_down.Suite.client(CLIENT_TEST_DIR)
        act = "succeeded" if loc_res else "failed"
        cls.log.info("Client teardown %s" % act)
        # Tear down server
        cls.bridge.send(SERVER_TEST_DIR, tear_down)
        rem_res = cls.bridge.remote_shell(cls.bridge.python, SERVER_TEST_DIR,
                                          tear_down, cls.ex_opts)
        act = "succeeded" if rem_res.succeeded else "failed"
        cls.log.info("Server teardown %s" % act)
        cls.bridge.remove(SERVER_TEST_DIR)

    def setup_method(self, method):
        """ Description """
        cls = self.__class__
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP(method.__name__, '-'))
        # set up server
        server_test_file = os.path.join(SERVER_TEST_DIR, cls.test_file)
        create = cls.bridge.sudo("touch %s" % server_test_file)
        act = "succeeded" if create.succeeded else "failed"
        cls.log.info("Server setup %s" % act)
        # set up client
        mount = set_up.Case.client(CLIENT_TEST_DIR)
        act = "succeeded" if mount else "failed"
        cls.log.info("Client setup %s" % act)

    def teardown_method(self, method):
        """ Description """
        cls = self.__class__
        # tear down client
        umount = tear_down.Case.client(CLIENT_TEST_DIR)
        act = "succeeded" if umount else "failed"
        cls.log.info("Client teardown %s" % act)
        # tear down server
        server_test_file = os.path.join(SERVER_TEST_DIR, cls.test_file)
        remove = cls.bridge.sudo("rm %s" % server_test_file)
        act = "succeeded" if remove.succeeded else "failed"
        cls.log.info("Server teardown %s" % act)


class AccessSuite(Suite):
    """ Description """

    def test_creation(self):
        """ Description """
        cls = self.__class__
        #
        client_test_file = os.path.join(CLIENT_TEST_DIR, cls.test_file)
        new_file = '.'.join((client_test_file, 'new'))
        try:
            open(new_file, 'w').close()
            cls.log.info("Created - %s" % new_file)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not Created - %s" % new_file)
            cls.log.info(cls.error_meaning)

    def test_edition(self):
        """ Description """
        cls = self.__class__
        #
        client_test_file = os.path.join(CLIENT_TEST_DIR, cls.test_file)
        try:
            with open(client_test_file, 'w') as file:
                file.write(client_test_file)
            cls.log.info("Edited - %s" % client_test_file)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not edited - %s" % client_test_file)
            cls.log.info(cls.error_meaning)

    def test_deletion(self):
        """ Description """
        cls = self.__class__
        #
        client_test_file = os.path.join(CLIENT_TEST_DIR, cls.test_file)
        try:
            os.remove(client_test_file)
            cls.log.info("Deleted - %s" % client_test_file)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not deleted - %s" % client_test_file)
            cls.log.info(cls.error_meaning)
