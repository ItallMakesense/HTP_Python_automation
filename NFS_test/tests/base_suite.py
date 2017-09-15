"""
Module keeps the basic test suite (actually two) for all of the made test cases
"""

import pytest

from config import *
from config import __file__ as config_file
from bridge import Bridge
import common
import set_up
import tear_down


DEBUG_LOG = common.initiate_logger(DEBUG_LOG)
CMD_LOG = common.initiate_logger(LOC_CMD_LOG)


def extract_args(options):
    """
    Gets `options` from command line of test execution, using `Pytest`
    special method
    """
    for opt in options:
        yield pytest.config.getoption(opt)


class Suite:
    """
    Represents general structure of every test suite in this package,
    thus serves as parent class for them.
    Contains common setup and teardown methods for class level, and same for
    methods level
    """

    # Dummy attributes. It must be changed in child test suites
    log, ex_opts, test_file, error_meaning, success_meaning = range(5)

    # Getting arguments from command line
    server_pswd, client_dir, server_dir = extract_args(
        [REM_PASS_OP, LOC_DIR_OP, REM_DIR_OP])

    # Function for text interpretation of given boolean value
    result = lambda succeeded: "succeeded" if succeeded else "failed"

    @classmethod
    def prepare(cls, logger, exports, header):
        """
        Assosiates given `logger` and `exports` options with appropriate
        class attributes, writes major `header` with this class `setup`
        header to the given logger and `DEBUG_LOG`
        """
        cls.log = logger
        cls.ex_opts = exports
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP(header))
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s setup" % cls.__name__, '_'))

    @classmethod
    def setup_class(cls):
        """
        Test setup for a class level (will run once for all methods in class).

        Setup nfs server: creates test folder, sends modules,
        needed for server setup, executes them (read `set_up.Suite.server`
        description) and finally removes sended mudules.

        Setup nfs client: executes `set_up.Suite.client` (read description).

        Writes setup results to the current test log
        """
        cls.bridge = Bridge(cls.server_pswd)
        # Set up server
        cls.bridge.sudo('mkdir %s' % cls.server_dir)
        cls.bridge.send([config_file, common.__file__, set_up.__file__],
                        cls.server_dir)
        rem_res = cls.bridge.remote_shell(cls.bridge.python, cls.server_dir,
                                          set_up, cls.ex_opts)
        cls.log.info("Server setup %s" % cls.result(rem_res.succeeded))
        cls.bridge.remove(cls.server_dir, only_files=True)
        # Set up client
        loc_res = set_up.Suite.client(cls.client_dir)
        cls.log.info("Client setup %s" % cls.result(loc_res))

    @classmethod
    def teardown_class(cls):
        """
        Test teardown for a class level (will run once for all methods in class).

        Teardown nfs client: executes `tear_down.Suite.client` (read description).

        Teardown nfs server: sends modules, needed for server teardown,
        executes them (read `tear_down.Suite.server` description) and
        finally removes test folder.

        Writes teadown results to the current test log
        """
        # Tear down client
        loc_res = tear_down.Suite.client(cls.client_dir)
        cls.log.info("Client teardown %s" % cls.result(loc_res))
        # Tear down server
        cls.bridge.send([config_file, common.__file__, tear_down.__file__],
                        cls.server_dir)
        rem_res = cls.bridge.remote_shell(cls.bridge.python, cls.server_dir,
                                          tear_down, cls.ex_opts)
        cls.log.info("Server teardown %s" % cls.result(rem_res.succeeded))
        cls.bridge.remove(cls.server_dir)

    def setup_method(self, method):
        """
        Test setup for a method level (will run for every method in class).

        Writes header with this method's name to the test log and `DEBUG_LOG`.
        Setup nfs server: creates test file.
        Setup nfs client: executes `set_up.Case.client` (read description).
        Writes setup results to the current test log
        """
        cls = self.__class__
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP(method.__name__, '-'))
        # set up server
        server_test_file = os.path.join(cls.server_dir, cls.test_file)
        create = cls.bridge.sudo("touch %s" % server_test_file)
        cls.log.info("Server setup %s" % cls.result(create.succeeded))
        # set up client
        mount = set_up.Case.client(cls.server_dir, cls.client_dir)
        cls.log.info("Client setup %s" % cls.result(mount))

    def teardown_method(self):
        """
        Test teardown for a method level (will run once for every method in class).

        Teardown nfs client: executes `tear_down.Case.client` (read description).
        Teardown nfs server: removes test file.
        Writes teadown results to the current test log
        """
        cls = self.__class__
        # tear down client
        umount = tear_down.Case.client(cls.client_dir)
        cls.log.info("Client teardown %s" % cls.result(umount))
        # tear down server
        server_test_file = os.path.join(cls.server_dir, cls.test_file)
        find = cls.bridge.sudo("test -e %s" % server_test_file)
        if find.succeeded:
            remove = cls.bridge.sudo("rm %s" % server_test_file)
            cls.log.info("Server teardown %s" % cls.result(remove.succeeded))


class AccessSuite(Suite):
    """
    Represents general structure of tests cases in this package, that checking
    file access permissions, thus serves as parent class for them.

    Contains common setup and teardown methods for class level, and same for
    methods level. Also contains separate test units for this type of test cases
    """

    # Getting test file name from command line of test execution
    test_file, = extract_args([TEST_FILE_OP])

    @classmethod
    def setup_class(cls, logger, exports, header, expect_fail=False):
        """
        Assosiates appropriate class attributes accordingly `expect_fail`,
        runs `base_suite.Suite.prepare` method with given `logger`, `exports`
        and `header` arguments (read vdescription)

        Finally runs inherited `base_suite.Suite.setup_class`
        """
        cls.success_meaning = "Test failed" if expect_fail else "Test passed"
        cls.error_meaning = "Test passed" if expect_fail else "Test failed"
        cls.prepare(logger, exports, header)
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        """
        Writes header with this class' `teardown` header to the test log
        and `DEBUG_LOG`.

        Finally runs inherited `base_suite.Suite.teardown_class`
        """
        common.write_to([cls.log.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s teardown" % cls.__name__, '_'))
        super().teardown_class()

    def test_creation(self):
        """
        Tests nfs client's access permission for the nfs server's test folder,
        that was mounted locally, by creating new file
        """
        cls = self.__class__
        client_test_file = os.path.join(cls.client_dir, cls.test_file)
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
        """
        Tests nfs client's access permission for the nfs server's test folder,
        that was mounted locally, by editing test file, created during
        current test setup
        """
        cls = self.__class__
        client_test_file = os.path.join(cls.client_dir, cls.test_file)
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
        """
        Tests nfs client's access permission for the nfs server's test folder,
        that was mounted locally, by removing test file, created during
        current test setup
        """
        cls = self.__class__
        #
        client_test_file = os.path.join(cls.client_dir, cls.test_file)
        try:
            os.remove(client_test_file)
            cls.log.info("Deleted - %s" % client_test_file)
            cls.log.info(cls.success_meaning)
        except Exception as error:
            DEBUG_LOG.error(error)
            cls.log.info("Not deleted - %s" % client_test_file)
            cls.log.info(cls.error_meaning)
