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
        self.assertEqual(len(self.account.wallets), 3)



if __name__ == '__main__':
    unittest.main()