import unittest
from enviro import home_path, client_username, client_password
from main import executor


class OwnerTest(unittest.TestCase):

    def setUp(self):
        executor(
            "bash -c \"useradd test_user; echo -e \'test\ntest\' | passwd test_user\"")

    def test_main_user(self):
        edit = True
        errors_getter = executor(
            "bash -c \'echo check >> /mnt/test_nfs/edition_check\'")
        print(errors_getter.lower())
        if 'denied' in errors_getter.lower():
            edit = False
        self.assertEqual(edit, True)

    def test_user(self):
        edit = False
        errors_getter = executor(
            "runuser -l test_user -c \"bash -c \'echo check >> /mnt/test_nfs/edition_check\'\"")
        print(errors_getter.lower())
        if 'denied' in errors_getter.lower():
            print('here')
            edit = True
        self.assertEqual(edit, True)

    def tearDown(self):
        executor("bash -c \"userdel test_user\"")
