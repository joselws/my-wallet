import json
import os
from Account import Account
from Wallet import Wallet
import unittest


class TestAccount(unittest.TestCase):
    """
    To test the account class, change the wallet_name 
    to test_wallet.json, there is all the test data located
    """

    def setUp(self):
        self.account = Account('Jose')
        self.main = self.account.get_wallet('main')
        self.emergencies = self.account.get_wallet('emergencies')
        self.charity = self.account.get_wallet('charity')


    def test_account_correctly_created(self):
        """Test that the account was correctly created"""
        self.assertTrue(os.path.exists(self.account.wallet_name))
        self.assertEqual(self.account.owner, 'Jose')
        self.assertEqual(len(self.account.wallets), 3)

        self.assertEqual(self.main.name, 'main')
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.main.percent, 70)
        self.assertIsNone(self.main.cap)

        self.assertEqual(self.emergencies.name, 'emergencies')
        self.assertEqual(self.emergencies.balance, 500)
        self.assertEqual(self.emergencies.percent, 20)
        self.assertEqual(self.emergencies.cap, 50000)

        self.assertEqual(self.charity.name, 'charity')
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.charity.percent, 10)
        self.assertIsNone(self.charity.cap)

    def test_get_wallet(self):
        """Test the get_wallet method"""
        self.assertEqual(self.main.name, 'main')
        self.assertEqual(self.emergencies.name, 'emergencies')
        self.assertEqual(self.charity.name, 'charity')
        with self.assertRaises(Exception):
            self.account.get_wallet('travels')

    def test_add_wallet(self):
        """Test the add wallet feature"""
        new_wallet = Wallet('home', 150, 5, 2000)
        self.account.add_wallet(new_wallet)
        self.assertEqual(len(self.account.wallets), 4)

        got_wallet = self.account.get_wallet('home')
        self.assertEqual(got_wallet.name, 'home')
        self.assertEqual(got_wallet.balance, 150)
        self.assertEqual(got_wallet.percent, 5)
        self.assertEqual(got_wallet.cap, 2000)


if __name__ == '__main__':
    unittest.main()