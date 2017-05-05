import unittest
import logging
from enviro import home_path, client_username, client_password, executor


logger = logging.getLogger("tests_log")
errors_logger = logging.getLogger("tests_log.stderr")

class OwnerTest(unittest.TestCase):

    def setUp(self):
        logger.info("______NFS folder user access permission test began______")
        logger.info("New client user creation.")
        result = executor(
            "bash -c \"useradd test_user; echo -e \'test\ntest\' | passwd test_user\"")
        if "successfull" in result:
            errors_logger.info(result.strip())
            logger.info("\t\tUser created.")
        else:
            errors_logger.info(result.strip())
            logger.info("\t\tUser haven't been created. Check enviro.log.")

    def test_main_user(self):
        logger.info("Main user permission test began.")
        edit = True
        errors_getter = executor(
            "bash -c \'echo check >> /mnt/test_nfs/edition_check\'")
        if 'denied' in errors_getter.lower():
            edit = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        elif not errors_getter:
            logger.info("\t\tTest passed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        self.assertEqual(edit, True)

    def test_user(self):
        logger.info("Newly created user permission test began.")
        edit = True
        errors_getter = executor(
            "runuser -l test_user -c \"bash -c \'echo check >> /mnt/test_nfs/edition_check\'\"")
        if 'denied' in errors_getter.lower():
            edit = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        elif not errors_getter:
            logger.info("\t\tTest failed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        self.assertEqual(edit, False)

    def tearDown(self):
        logger.info("Deletion of the created user...")
        result = executor("bash -c \"userdel test_user\"")
        if not result:
            logger.info("\t\tUser deleted.")
        else:
            errors_logger.info(result.strip())
            logger.info("\t\tUser haven't been deleted. Check enviro.log.")
