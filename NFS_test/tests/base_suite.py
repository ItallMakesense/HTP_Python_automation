"""
Description
"""

import logging
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
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Server setup", '_'))
        #
        cls.bridge = Bridge(cls)
        # Set up server
        cls.bridge.prepare(SERVER_TEST_DIR)
        cls.bridge.send(SERVER_TEST_DIR, set_up)
        result = cls.bridge.remote_shell('python3', SERVER_TEST_DIR, set_up,
                                         ','.join(cls.ex_opts))
        if result.succeeded:
            cls.log.info("Setup succeeded")
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], result)
        cls.bridge.remove(SERVER_TEST_DIR, only_files=True)
        #
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Client setup", '_'))
        # Set up client
        set_up.Suite.client(CLIENT_TEST_DIR, cls.log)

    @classmethod
    def teardown_class(cls):
        """ Description """
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Client teardown", '_'))
        # Tear down client
        tear_down.Suite.client(CLIENT_TEST_DIR, cls.log)

        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Server teardown", '_'))
        
        # Tear down server
        cls.bridge.send(SERVER_TEST_DIR, tear_down)
        result = cls.bridge.remote_shell('python3', SERVER_TEST_DIR, tear_down,
                                         ','.join(cls.ex_opts))
        if result.succeeded:
            cls.log.info("Teardown succeeded")
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], result)
        cls.bridge.remove(SERVER_TEST_DIR)

    def setup_method(self, method):
        """ Description """
        cls = self.__class__
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s setup" % method.__name__, '-'))
        # set up server
        server_test_file = os.path.join(SERVER_TEST_DIR, cls.test_file)
        create = cls.bridge.sudo("touch %s" % server_test_file)
        if create.succeeded:
            cls.log.info("Created - %s" % ':'.join((SERVER_ADDRESS, server_test_file)))
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], create)
        # set up client
        set_up.Case.client(CLIENT_TEST_DIR, cls.log)

    def teardown_method(self, method):
        """ Description """
        cls = self.__class__
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s teardown" % method.__name__, '-'))
        # tear down client
        tear_down.Case.client(CLIENT_TEST_DIR, cls.log)
        # tear down server
        server_test_file = os.path.join(SERVER_TEST_DIR, cls.test_file)

        remove = cls.bridge.sudo("rm %s" % server_test_file)
        if remove.succeeded:
            cls.log.info("Removed - %s" % server_test_file)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], remove)


class AccessSuite(Suite):
    """ Description """

    def test_creation(self):
        """ Description """
        cls = self.__class__
        cls.log.info("Creation test".center(80, '.'))
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
        cls.log.info("Edition test".center(80, '.'))
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
        cls.log.info("Deletion test".center(80, '.'))
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
