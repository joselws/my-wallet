import json
import os
from Account import Account
import unittest


class TestAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.filepath = os.getcwd() + '/test_wallet.json'

    def setUp(self):
        self.account = Account('Jose')


    def test_json_file_exists(self):
        self.assertTrue(os.path.exists(self.filepath))


if __name__ == '__main__':
    unittest.main()