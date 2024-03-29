import json
import os
from Account import Account
import unittest
from Wallet import Wallet


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account("test_empty_wallet.json")


    def test_json_file_exists(self):
        self.assertTrue(os.path.exists(self.account.get_wallet_name()))
    
    def test_account_created(self):
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

        new_acc = Account("test_empty_wallet.json")
        self.assertTrue(os.path.exists(self.account.get_wallet_name()))

    def test_transactions_file_correctly_created(self):
        os.remove(self.account.get_transactions_file_name())
        self.assertFalse(os.path.exists(self.account.get_transactions_file_name()))

        new_acc = Account("test_empty_wallet.json")
        self.assertTrue(os.path.exists(self.account.get_transactions_file_name()))

    def test_transactions_file_has_right_headers(self):
        os.remove(self.account.get_transactions_file_name())
        new_acc = Account("test_empty_wallet.json")
        headers = "date,wallet,transaction_type,amount,description,balance_before,balance_after\n"
        with open(self.account.get_transactions_file_name(), "r") as file:
            contents = file.read()
        self.assertEqual(contents, headers)

    
if __name__ == '__main__':
    acc = Account("test_empty_wallet.json")
    if (
        acc.get_wallet_name() == "test_empty_wallet.json"
        and acc.get_transactions_file_name() == "test_transactions.csv"
    ):
        unittest.main(buffer=True)
    else:
        print("You're not using your test empty wallet or test transactions!")