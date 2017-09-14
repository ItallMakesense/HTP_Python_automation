"""
Module keeps test suite for checking nfs client's user access permission.

To change the class' attributes, defined through command line arguments
(for example, nfs server test file) directly in this module
(not with `config.py` or through those command line arguments), simply redefine
them in the class body after their extraction by `extract_args`
"""

import logging
import pytest

from config import *
import common
from .base_suite import Suite, extract_args


DEBUG_LOG = logging.getLogger(DEBUG_LOG)
LOG = common.initiate_logger(OWN_TEST_LOG)


class TestOwner(Suite):
    """
    Test case for checking nfs client's user access permission for the mounted
    test folder from nfs server
    """

    # Getting arguments from command line
    client_pswd, test_file, test_user = extract_args(
        [LOC_PASS_OP, TEST_FILE_OP, TEST_USER_OP])

    @classmethod
    def user_action(cls, cmd, msg):
        """
        Used for quick execution of user creation and removing in this test case.
        Also writes `msg` (about success), if operation was successfull
        """
        result = common.execute(['sudo', '-S', cmd, cls.test_user],
                                collect=True, input_line=cls.client_pswd)
        if result[2]:  # Exit code
            LOG.info("%s - %s" % (msg, cls.test_user))

    @classmethod
    def setup_class(cls):
        """
        Runs `base_suite.Suite.prepare` with this test case arguments
        (read description), then creates user with `cls.test_user` name.

        Finally runs inherited `base_suite.Suite.setup_class`
        """
        cls.prepare(LOG, OWN_EXPORTS, "NFS test - various users access")
        cls.user_action('useradd', 'Created')
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        """
        Writes header with this class' `teardown` header to the test log
        and `DEBUG_LOG`, removes user, created in setup.

        Finally runs inherited `base_suite.Suite.setup_class`
        """
        common.write_to([LOG.info, DEBUG_LOG.info],
                        common.MAKE_CAP("%s teardown" % cls.__name__, '_'))
        cls.user_action('userdel', 'Removed')
        super().teardown_class()

    def test_existing_user(self):
        """
        Tests access permission of existing user for the nfs server's
        test folder, that was mounted, by editing test file, created during
        current test setup
        """
        cls = self.__class__
        client_test_file = os.path.join(cls.client_dir, cls.test_file)
        try:
            open(client_test_file, 'w').close()
            cls.log.info("Access %s - %s" % (True, client_test_file))
            cls.log.info("Test passed")
        except:
            cls.log.info("Access %s - %s" % (False, client_test_file))
            cls.log.info("Test failed")
            assert False

    def test_new_user(self):
        """
        Tests access permission of new user, created during test case setup,
        for the nfs server's test folder, that was mounted, by editing test file
        """
        cls = self.__class__
        client_test_file = os.path.join(cls.client_dir, cls.test_file)
        access = common.execute('sudo -S runuser -l {user} -c \"touch {file}\"'
                                .format(user=cls.test_user, file=client_test_file),
                                shell=True, collect=True, input_line=cls.client_pswd)
        cls.log.info("Access %s - %s" % (access[2], client_test_file))
        cls.log.info("Test passed" if not access[2] else "Test failed")
        assert not access[2], "%s - access denied" % cls.test_user
