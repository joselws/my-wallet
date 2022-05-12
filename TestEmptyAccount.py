import json
import os
from Account import Account
import unittest


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('Jose')


    def test_json_file_exists(self):
        self.assertTrue(os.path.exists(self.account.wallet_name))
    
    def test_account_created(self):
        self.assertEqual(self.account.owner, 'Jose')
        self.assertEqual(self.account.wallets, [])

    def test_wallet_file_initialized(self):
        with open(self.account.wallet_name) as file:
            json_content = file.read()
        self.assertEqual(json_content, '[]')


if __name__ == '__main__':
    unittest.main()