import json
import os
from Account import Account
import unittest


class TestAccount(unittest.TestCase):
    """
    To test the account class, change the wallet_name 
    to test_wallet.json, there is all the test data located
    """

    def setUp(self):
        self.account = Account('Jose')


    def test_account_correctly_created(self):
        """Test that the account was correctly created"""
        self.assertTrue(os.path.exists(self.account.wallet_name))
        self.assertEqual(self.account.owner, 'Jose')
        self.assertEqual(len(self.account.wallets), 3)

    def test_get_wallet(self):
        """Test the get_wallet method"""
        main = self.account.get_wallet('main')
        emergencies = self.account.get_wallet('emergencies')
        charity = self.account.get_wallet('charity')
        
        self.assertEqual(main.name, 'main')
        self.assertEqual(emergencies.name, 'emergencies')
        self.assertEqual(charity.name, 'charity')
        with self.assertRaises(Exception):
            self.account.get_wallet('travels')


if __name__ == '__main__':
    unittest.main()