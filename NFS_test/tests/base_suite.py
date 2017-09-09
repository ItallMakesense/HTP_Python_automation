"""
Description
"""

import logging

from config import *
import common
import bridge
import set_up
import tear_down


DEBUG_LOG, DEBUG_FILE = common.initiate_logger(DEBUG_LOG)

class Suite:
    """ Description """

    # Dummy attributes. Changing in child test suites
    log, ex_opts, test_file, error_meaning, success_meaning = range(5)

    @classmethod
    def setup_class(cls):
        """ Description """
        # Set up server
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Server setup", '_'))
        ## Creating test directory
        bridge.prepare(SERVER_TEST_DIR, cls.log)
        ## Sending setup files (and other)
        bridge.send(SERVER_TEST_DIR, set_up, cls.log)
        ## Executing setup on a server
        result = bridge.remote_shell('python3', SERVER_TEST_DIR, set_up,
                                     NFS_SERVER, ','.join(cls.ex_opts))
        if result.succeeded:
            cls.log.info("Setup succeeded")
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], result)
        ## Removing setup files
        remove = bridge.sudo("rm -r %s" % os.path.join(SERVER_TEST_DIR, '*'),
                             shell=False, shell_escape=True)
        if remove.succeeded:
            cls.log.info("Removed - %s" % os.path.join(SERVER_TEST_DIR, '*'))
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], remove)

        # Set up client
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Client setup", '_'))
        set_up.Suite.client(CLIENT_TEST_DIR, cls.log)

    @classmethod
    def teardown_class(cls):
        """ Description """
        # Tear down client
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Client teardown", '_'))
        tear_down.Suite.client(CLIENT_TEST_DIR, cls.log)

        # Tear down server
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("Server teardown", '_'))
        ## Sending teardown files (and other)
        bridge.send(SERVER_TEST_DIR, tear_down, cls.log)
        ## Executing setup on a server
        result = bridge.remote_shell('python3', SERVER_TEST_DIR, tear_down,
                                     NFS_SERVER, ','.join(cls.ex_opts))
        common.write_to([cls.log.debug, cls.log.error], result)
        ## Removing teardown files
        remove = bridge.sudo("rm -r %s" % SERVER_TEST_DIR, shell=False, shell_escape=True)
        if remove.succeeded:
            cls.log.info("Removed - %s" % SERVER_TEST_DIR)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], remove)

    def setup_method(self, method):
        """ Description """
        cls = self.__class__
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s setup" % method, '-'))
        # set up server
        create = bridge.sudo("touch %s" % cls.test_file, shell=False,
                             shell_escape=True)
        if create.succeeded:
            cls.log.info("Created - %s" % cls.test_file)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], create)
        # set up client
        set_up.Case.client(CLIENT_TEST_DIR, cls.log)

    def teardown_method(self, method):
        """ Description """
        cls = self.__class__
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s teardown" % method, '-'))
        # tear down client
        tear_down.Case.client(CLIENT_TEST_DIR, cls.log)
        # tear down server
        remove = bridge.sudo("rm %s" % cls.test_file, shell=False, shell_escape=True)
        if remove.succeeded:
            cls.log.info("Removed - %s" % cls.test_file)
        common.write_to([DEBUG_LOG.debug, DEBUG_LOG.error], remove)


class AccessSuite(Suite):
    """ Description """

    def test_creation(self):
        """ Description """
        cls = self.__class__
        new_file_path = '.'.join((cls.test_file, 'new'))
        #
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Creation test start"))
        try:
            open(new_file_path, 'w').close()
            cls.log.info("Created - %s" % new_file_path)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not Created - %s" % new_file_path)
            cls.log.info(cls.error_meaning)
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Creation test end"))

    def test_edition(self):
        """ Description """
        cls = self.__class__
        #
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Edition test start"))
        try:
            with open(cls.test_file, 'w') as file:
                file.write(cls.test_file)
            cls.log.info("Edited - %s" % cls.test_file)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not edited - %s" % cls.test_file)
            cls.log.info(cls.error_meaning)
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Edition test end"))

    def test_deletion(self):
        """ Description """
        cls = self.__class__
        #
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Deletion test start"))
        try:
            os.remove(cls.test_file)
            cls.log.info("Deleted - %s" % cls.test_file)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not deleted - %s" % cls.test_file)
            cls.log.info(cls.error_meaning)
        common.write_to([cls.log.info, DEBUG_LOG.info], common.MAKE_CAP("Deletion test end"))
