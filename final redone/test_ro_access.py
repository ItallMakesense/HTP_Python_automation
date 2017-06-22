from sub import test_log_name, log_cap
from environment import client_execute
import unittest
import logging


log = logging.getLogger(test_log_name)

class ReadOnlyTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        log_cap(log.info, "NFS folder \"read-only\" attributes test began")

    def test_first_create(self):
        log_cap(log.info, "File creation test began", filler='-')
        create = True
        result, errors = client_execute(\
                         "bash -c \'> /mnt/test_ro_nfs/creation_check\'")
        if 'read-only' in errors.lower():
            create = False
            log.error(errors.strip())
            log.info("Test passed")
        elif not errors:
            log.info("Test failed")
        else:
            log.error(errors.strip())
            log.info("Test failed")
        self.assertEqual(create, False)

    def test_second_edit(self):
        log_cap(log.info, "File edition test began", filler='-')
        edit = True
        result, errors = client_execute("bash -c \'echo check >> " +\
                                "/mnt/test_ro_nfs/edition_check\'")
        if 'read-only' in errors.lower():
            edit = False
            log.error(errors.strip())
            log.info("Test passed")
        elif not errors:
            log.info("Test failed")
        else:
            log.error(errors.strip())
            log.info("Test failed")
        self.assertEqual(edit, False)

    def test_third_delete(self):
        log_cap(log.info, "File deletion test began", filler='-')
        delete = True
        result, errors = client_execute("rm /mnt/test_ro_nfs/creation_check")
        if 'no such file' in errors.lower():
            delete = False
            log.error(errors.strip())
            log.info("Test passed")
        elif not errors:
            log.info("Test failed")
        else:
            log.error(errors.strip())
            log.info("Test failed")
        self.assertEqual(delete, False)
