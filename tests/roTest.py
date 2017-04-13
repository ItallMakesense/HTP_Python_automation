import unittest
from main import executor

class ReadOnlyTest(unittest.TestCase):

    def test_first_create(self):
        create = True
        errors_getter = executor("bash -c \'> /mnt/test_ro_nfs/creation_check\'")
        if 'read-only' in errors_getter.lower():
            create = False
        self.assertEqual(create, False)

    def test_second_edit(self):
        edit = True
        errors_getter = executor("bash -c \'echo check >> /mnt/test_ro_nfs/edition_check\'")
        if 'read-only' in errors_getter.lower():
            edit = False
        self.assertEqual(edit, False)

    def test_third_delete(self):
        delete = True
        errors_getter = executor("rm /mnt/test_nfs/creation_check")
        if 'No such file' in errors_getter.lower():
            delete = False
        self.assertEqual(delete, False)