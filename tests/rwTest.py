import unittest
import logging
from enviro import executor


logger = logging.getLogger("tests_log")
errors_logger = logging.getLogger("tests_log.stderr")

class ReadWriteTest(unittest.TestCase):

    def test_first_create(self):
        logger.info("______NFS folder \"read-write\" attributes test began______")
        logger.info("File creation test began.")
        create = True
        errors_getter = executor("bash -c \'> /mnt/test_nfs/creation_check\'")
        if 'read-only' in errors_getter.lower():
            create = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        elif not errors_getter:
            logger.info("\t\tTest passed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        self.assertEqual(create, True)

    def test_second_edit(self):
        logger.info("File edition test began.")
        edit = True
        errors_getter = executor("bash -c \'echo check >> /mnt/test_nfs/edition_check\'")
        if 'read-only' in errors_getter.lower():
            edit = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        elif not errors_getter:
            logger.info("\t\tTest passed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        self.assertEqual(edit, True)

    def test_third_delete(self):
        logger.info("File deletion test began.")
        delete = True
        errors_getter = executor("rm /mnt/test_nfs/creation_check")
        if 'read-only' in errors_getter.lower():
            delete = False
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest failed.")
        elif not errors_getter:
            logger.info("\t\tTest passed.")
        else:
            errors_logger.info(errors_getter.strip())
            logger.info("\t\tTest passed.")
        self.assertEqual(delete, True)
