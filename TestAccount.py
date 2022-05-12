import json
import os
from Account import Account
import unittest


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('Jose')


    def test_account_correctly_created(self):
        self.assertTrue(os.path.exists(self.account.wallet_name))
        self.assertEqual(self.account.owner, 'Jose')
        self.assertEqual(len(self.account.wallets), 3)


if __name__ == '__main__':
    unittest.main()