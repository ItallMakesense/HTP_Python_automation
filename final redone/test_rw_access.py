from sub import test_log_name, log_cap
from environment import client_execute
import unittest
import logging


log = logging.getLogger(test_log_name)

class ReadWriteTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        log_cap(log.info,"NFS folder \"read-write\" attributes test began")

    def test_first_create(self):
        log_cap(log.info, "File creation test began", filler='-')
        create = True
        result, errors = client_execute(\
                         "bash -c \'> /mnt/test_nfs/creation_check\'")
        if 'read-only' in errors.lower():
            create = False
            log.error(errors.strip())
            log.info("Test failed")
        elif not errors:
            log.info("Test passed")
        else:
            log.error(errors.strip())
            log.info("Test passed")
        self.assertEqual(create, True)

    def test_second_edit(self):
        log_cap(log.info, "File edition test began", filler='-')
        edit = True
        result, errors = client_execute("bash -c \'echo check >> " +\
                                "/mnt/test_nfs/edition_check\'")
        if 'read-only' in errors.lower():
            edit = False
            log.error(errors.strip())
            log.info("Test failed")
        elif not errors:
            log.info("Test passed")
        else:
            log.error(errors.strip())
            log.info("Test passed")
        self.assertEqual(edit, True)

    def test_third_delete(self):
        log_cap(log.info, "File deletion test began", filler='-')
        delete = True
        result, errors = client_execute("rm /mnt/test_nfs/creation_check")
        if 'read-only' in errors.lower():
            delete = False
            log.error(errors.strip())
            log.info("Test failed")
        elif not errors:
            log.info("Test passed")
        else:
            log.error(errors.strip())
            log.info("Test passed")
        self.assertEqual(delete, True)
