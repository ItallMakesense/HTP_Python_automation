import unittest
import logging
from enviro import executor


logger = logging.getLogger("tests_log")
errors_logger = logging.getLogger("tests_log.stderr")

class ReadOnlyTest(unittest.TestCase):

    def test_first_create(self):
        logger.info("______NFS folder \"read-only\" attributes test began______")
        logger.info("File creation test began.")
        create = True
        errors_getter = executor("bash -c \'> /mnt/test_ro_nfs/creation_check\'")
        if 'read-only' in errors_getter.lower():
            create = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        elif not errors_getter:
            logger.info("\t\tTest failed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        self.assertEqual(create, False)

    def test_second_edit(self):
        logger.info("File edition test began.")
        edit = True
        errors_getter = executor("bash -c \'echo check >> /mnt/test_ro_nfs/edition_check\'")
        if 'read-only' in errors_getter.lower():
            edit = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        elif not errors_getter:
            logger.info("\t\tTest failed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        self.assertEqual(edit, False)

    def test_third_delete(self):
        logger.info("File deletion test began.")
        delete = True
        errors_getter = executor("rm /mnt/test_nfs/creation_check")
        if 'no such file' in errors_getter.lower():
            delete = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        elif not errors_getter:
            logger.info("\t\tTest failed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        self.assertEqual(delete, False)
