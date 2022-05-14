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
        self.assertFalse(self.main.cap)

        self.assertEqual(self.emergencies.name, 'emergencies')
        self.assertEqual(self.emergencies.balance, 500)
        self.assertEqual(self.emergencies.percent, 20)
        self.assertEqual(self.emergencies.cap, 50000)

        self.assertEqual(self.charity.name, 'charity')
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.charity.percent, 10)
        self.assertFalse(self.charity.cap)

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

        with self.assertRaises(Exception):
            self.account.add_wallet(Wallet('home'))

    def test_delete_wallet(self):
        """Test the delete wallet feature"""
        self.account.delete_wallet('charity')
        self.assertEqual(len(self.account.wallets), 2)
        with self.assertRaises(Exception):
            self.account.delete_wallet('charity')

    def test_correct_percent(self):
        """Test the correct percent feature"""
        self.assertTrue(self.account.correct_percent())

        test_account = Account('test')
        test_account.wallets.clear()
        test_account.add_wallet(Wallet('new1', 100, 20))
        test_account.add_wallet(Wallet('new2', 100))
        test_account.add_wallet(Wallet('new3', 100))
        test_account.add_wallet(Wallet('new4', 100, 50))

        test_account2 = Account('test2')
        test_account2.wallets.clear()
        test_account2.add_wallet(Wallet('new5'))
        test_account2.add_wallet(Wallet('new6'))
        self.assertFalse(test_account2.correct_percent())

    def test_valid_number(self):
        """Tests for the valid_number method"""
        self.assertTrue(self.account.valid_number(10))
        self.assertFalse(self.account.valid_number(0))
        self.assertFalse(self.account.valid_number('10'))
        self.assertFalse(self.account.valid_number(4.3))
        self.assertFalse(self.account.valid_number(-9))
        self.assertFalse(self.account.valid_number(True))
        self.assertFalse(self.account.valid_number(None))

    def test_transfer(self):
        """Tests for the transfer feature"""
        self.account.transfer('main', 'emergencies', 500)
        self.assertEqual(self.main.balance, 1000)
        self.assertEqual(self.emergencies.balance, 1000)

        with self.assertRaises(Exception):
            self.account.transfer('charity', 'emergencies', 300)

        with self.assertRaises(ValueError):
            self.account.transfer('main', 'charity', -50)

    def test_total(self):
        """Test Total method"""
        self.assertEqual(self.account.total(), '$2200')

    def test_save(self):
        """Save method correctly saves changes into JSON file"""
        # Save a new wallet to json file
        self.account.add_wallet(Wallet('test', 10, 10, 10))
        self.account.save()

        # read json file and confirm new wallet values
        account = Account('Jose')
        test = account.get_wallet('test')
        self.assertEqual(len(account.wallets), 4)
        self.assertEqual(test.name, 'test')
        self.assertEqual(test.balance, 10)
        self.assertEqual(test.percent, 10)
        self.assertEqual(test.cap, 10)

        # delete new wallet and save to json file
        account.delete_wallet('test')
        account.save()

        # read json file and confirm new wallet was deleted
        account = Account('Jose')
        self.assertEqual(len(account.wallets), 3)
        with self.assertRaises(Exception):
            test = account.get_wallet('test')

if __name__ == '__main__':
    unittest.main()