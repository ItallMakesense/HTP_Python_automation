import unittest
from main import executor

class ReadWriteTest(unittest.TestCase):

    def test_first_create(self):
        create = True
        errors_getter = executor("bash -c \'> /mnt/test_nfs/creation_check\'")
        if 'read-only' in errors_getter.lower():
            create = False
        self.assertEqual(create, True)

    def test_second_edit(self):
        edit = True
        errors_getter = executor("bash -c \'echo check >> /mnt/test_nfs/edition_check\'")
        if 'read-only' in errors_getter.lower():
            edit = False
        self.assertEqual(edit, True)

    def test_third_delete(self):
        delete = True
        errors_getter = executor("rm /mnt/test_nfs/creation_check")
        if 'read-only' in errors_getter.lower():
            delete = False
        self.assertEqual(delete, True)