"""
Test Case Name:
    test_owner.py

Description:
    Check user's access to the NFS folder on client machine

Pre-conditions:
    1. Paramiko is installed on server machine
    1. NFS folder is installed and mounted on client machine

Steps:
    1. 

Post-conditions:
    1.
"""

from sub import test_log_name, log_cap
from environment import client_execute
import unittest
import logging


log = logging.getLogger(test_log_name)

class OwnerTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        log_cap(log.info, "NFS folder user access permission test began")
        log.info("New client user creation")
        result, errors = client_execute("bash -c \"useradd test_user; " +\
                                "echo -e \'test\ntest\' | passwd test_user\"")
        log.error(errors.strip())
        if "successfull" in errors.lower():
            log.info("User created")
        else:
            log.info("User haven't been created. Check environment.info")

    @classmethod
    def tearDownClass(self):
        log.info("Deletion of the created user...")
        result, errors = client_execute("bash -c \"userdel test_user\"")
        if not errors:
            log.info("User deleted")
        else:
            log.error(errors.strip())
            log.info("User haven't been deleted. Check environment.info")

    def test_main_user(self):
        log_cap(log.info, "Main user permission test began", filler='-')
        edit = True
        result, errors = client_execute(
            "bash -c \'echo check >> /mnt/test_nfs/edition_check\'")
        if 'denied' in errors.lower():
            edit = False
            log.error(errors.strip())
            log.info("Test failed")
        elif not errors:
            log.info("Test passed")
        else:
            log.error(errors.strip())
            log.info("Test passed")
        self.assertEqual(edit, True)

    def test_user(self):
        log_cap(log.info, "Newly created user permission test began", filler='-')
        edit = True
        result, errors = client_execute("runuser -l test_user -c \"bash -c " +\
                            "\'echo check >> /mnt/test_nfs/edition_check\'\"")
        if 'denied' in errors.lower():
            edit = False
            log.error(errors.strip())
            log.info("Test passed")
        elif not errors:
            log.info("Test failed")
        else:
            log.error(errors.strip())
            log.info("Test failed")
        self.assertEqual(edit, False)
