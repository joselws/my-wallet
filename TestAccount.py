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
        self.account.add_wallet('home', 150, 5, 2000)
        new_wallet = self.account.get_wallet('home')
        self.assertEqual(len(self.account.wallets), 4)
        self.assertEqual(new_wallet.name, 'home')
        self.assertEqual(new_wallet.balance, 150)
        self.assertEqual(new_wallet.percent, 5)
        self.assertEqual(new_wallet.cap, 2000)

        with self.assertRaises(Exception):
            self.account.add_wallet('home')

        with self.assertRaises(Exception):
            self.account.add_wallet('test', 'hi')
        with self.assertRaises(Exception):
            self.account.add_wallet('test2', 200, 'hi')
        with self.assertRaises(Exception):
            self.account.add_wallet('test', 300, 10, 'hi')

    def test_delete_wallet(self):
        """Test the delete wallet feature"""
        self.account.delete_wallet('charity')
        self.assertEqual(len(self.account.wallets), 2)
        with self.assertRaises(Exception):
            self.account.delete_wallet('charity')

    def test_cant_delete_main(self):
        """Main wallet is not allowed to be deleted"""
        with self.assertRaises(Exception):
            self.account.delete_wallet('main')

    def test_correct_percent(self):
        """Test the correct percent feature"""
        self.assertTrue(self.account.correct_percent())

        test_account = Account('test')
        test_account.wallets.clear()
        test_account.add_wallet('new1', 100, 20)
        test_account.add_wallet('new2', 100)
        test_account.add_wallet('new3', 100)
        test_account.add_wallet('new4', 100, 50)

        test_account2 = Account('test2')
        test_account2.wallets.clear()
        test_account2.add_wallet('new5')
        test_account2.add_wallet('new6')
        self.assertFalse(test_account2.correct_percent())

    def test_valid_number(self):
        """Tests for the valid_number method"""
        self.assertTrue(self.account.valid_number(10))
        self.assertTrue(self.account.valid_number(0))
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

    def test_transfer_none_amount(self):
        """Test transfer method transfering all money when amount is None"""
        self.account.transfer('charity', 'emergencies')
        self.assertEqual(self.charity.balance, 0)
        self.assertEqual(self.emergencies.balance, 700)

    def test_total(self):
        """Test Total method"""
        self.assertEqual(self.account.total(), '$2200')

    def test_save(self):
        """Save method correctly saves changes into JSON file"""
        # Save a new wallet to json file
        self.account.add_wallet('test', 10, 10, 10)
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
        main = account.get_wallet('main')
        main -= 10
        account.save()

        # read json file and confirm new wallet was deleted
        account = Account('Jose')
        self.assertEqual(len(account.wallets), 3)
        with self.assertRaises(Exception):
            test = account.get_wallet('test')

    def test_deduct(self):
        """Deduct method correctly working"""
        self.account.deduct('main', 500)
        self.assertEqual(self.main.balance, 1000)

        with self.assertRaises(Exception):
            self.account.deduct('charity', 1000)

        with self.assertRaises(Exception):
            self.account.deduct('no_wallet', 200)

        with self.assertRaises(Exception):
            self.account.deduct('charity', 'hi')

        self.account.deduct('emergencies')
        self.assertEqual(self.emergencies.balance, 0)

    def test_deposit(self):
        """Deposit feature works correctly"""
        self.account.deposit(1000)
        self.assertEqual(self.main.balance, 2200)
        self.assertEqual(self.emergencies.balance, 700)
        self.assertEqual(self.charity.balance, 300)

        with self.assertRaises(ValueError):
            self.account.deposit('twenty bucks')

    def test_add(self):
        """Add to wallet feature works correctly"""
        self.account.add('main', 500)
        self.assertEqual(self.main.balance, 2000)
        with self.assertRaises(Exception):
            self.account.add('no wallet', 20)
        with self.assertRaises(Exception):
            self.account.add('main', 'hi')

if __name__ == '__main__':
    unittest.main()