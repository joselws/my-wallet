import json
import os
from Account import Account
import unittest
from Wallet import Wallet


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('Jose')


    def test_json_file_exists(self):
        self.assertTrue(os.path.exists(self.account.get_wallet_name()))
    
    def test_account_created(self):
        self.assertEqual(self.account.owner, 'Jose')
        self.assertEqual(len(self.account.wallets), 1)

    def test_wallet_file_initialized(self):
        with open(self.account.get_wallet_name()) as file:
            json_content = file.read()
        wallets = json.loads(json_content)
        main = Wallet(**wallets[0])
        self.assertEqual(main.name, 'main')
        self.assertFalse(main.percent)
        self.assertFalse(main.balance)
        self.assertFalse(main.cap)

    def test_wallet_correctly_created(self):
        os.remove(self.account.get_wallet_name())
        self.assertFalse(os.path.exists(self.account.get_wallet_name()))

        new_acc = Account('new')
        self.assertTrue(os.path.exists(self.account.get_wallet_name()))


if __name__ == '__main__':
    unittest.main()