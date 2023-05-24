import unittest
import os
from AccountTransactionHandler import AccountTransactionHandler


class TestAccountTransactionHandler(unittest.TestCase):
    
    def setUp(self):
        AccountTransactionHandler._empty_queued_transactions()
        self.transaction_filename = "test_transactions.csv"
        with open(self.transaction_filename, "w") as file:
            file.write(AccountTransactionHandler.headers)


    def test_empty_queued_transactions(self):
        """List of queued transactions are emptied"""
        AccountTransactionHandler._transactions.extend([1, 2, 3])
        self.assertEqual(len(AccountTransactionHandler._transactions), 3)

        AccountTransactionHandler._empty_queued_transactions()
        self.assertEqual(len(AccountTransactionHandler._transactions), 0)

    def test_empty_no_queued_transactions(self):
        """List of queued transactions doesn't raise error when already empty"""
        AccountTransactionHandler._empty_queued_transactions()
        self.assertEqual(len(AccountTransactionHandler._transactions), 0)

    def test_show_queued_transactions(self):
        """Queued transactions are shown in standard output if they exist"""
        AccountTransactionHandler._transactions.extend([1, 2, 3])
        self.assertTrue(AccountTransactionHandler._show_queued_transactions())

    def test_show_queued_transactions_empty(self):
        """Shows error message when there are no queued transactions to show"""
        self.assertFalse(AccountTransactionHandler._show_queued_transactions())

    def test_queue_transaction(self):
        """Transactions are queued correctly"""
        date1 = "12-06-1995 00:00:00"
        wallet1 = "test_wallet_1"
        transaction_type = "deduction"
        amount1 = 20
        balance_before1 = 50
        balance_after1 = 30
        description1 = "test_description_1"
        entry1 = "12-06-1995 00:00:00,test_wallet_1,deduction,20,test_description_1,50,30\n"
        AccountTransactionHandler._queue_transaction(
            date=date1,
            wallet=wallet1,
            transaction_type=transaction_type,
            amount=amount1,
            balance_before=balance_before1,
            balance_after=balance_after1,
            description=description1
        )
        self.assertEqual(len(AccountTransactionHandler._transactions), 1)
        self.assertEqual(AccountTransactionHandler._transactions[0], entry1)
        
        date2 = "12-06-1996 00:00:00"
        wallet2 = "test_wallet_2"
        amount2 = 50
        balance_before2 = 90
        balance_after2 = 40
        description2 = "test_description_2"
        entry2 = "12-06-1996 00:00:00,test_wallet_2,deduction,50,test_description_2,90,40\n"
        AccountTransactionHandler._queue_transaction(
            date=date2,
            wallet=wallet2,
            transaction_type=transaction_type,
            amount=amount2,
            balance_before=balance_before2,
            balance_after=balance_after2,
            description=description2
        )
        self.assertEqual(len(AccountTransactionHandler._transactions), 2)
        self.assertEqual(AccountTransactionHandler._transactions[0], entry1)
        self.assertEqual(AccountTransactionHandler._transactions[1], entry2)

    def test_queue_transaction_no_description(self):
        """Transactions are queued correctly"""
        date1 = "12-06-1995 00:00:00"
        wallet1 = "test_wallet_1"
        transaction_type = "deduction"
        amount1 = 20
        balance_before1 = 50
        balance_after1 = 30
        entry1 = "12-06-1995 00:00:00,test_wallet_1,deduction,20,no_description,50,30\n"
        AccountTransactionHandler._queue_transaction(
            date=date1,
            wallet=wallet1,
            transaction_type=transaction_type,
            amount=amount1,
            balance_before=balance_before1,
            balance_after=balance_after1,
        )
        self.assertEqual(len(AccountTransactionHandler._transactions), 1)
        self.assertEqual(AccountTransactionHandler._transactions[0], entry1)

    def test_insert_transaction_error(self):
        """Returns False and do nothing if the transaction file doesn't exist"""
        os.remove(self.transaction_filename)
        self.assertFalse(AccountTransactionHandler._insert_queued_transactions(self.transaction_filename))
        self.assertFalse(os.path.exists(self.transaction_filename))

    def test_insert_transaction_success(self):
        """Queued transactions are put in the transactions file"""
        date1 = "12-06-1995 00:00:00"
        wallet1 = "test_wallet_1"
        transaction_type = "deduction"
        amount1 = 20
        balance_before1 = 50
        balance_after1 = 30
        description1 = "test_description_1"
        entry1 = "12-06-1995 00:00:00,test_wallet_1,deduction,20,test_description_1,50,30\n"
        AccountTransactionHandler._queue_transaction(
            date=date1,
            wallet=wallet1,
            transaction_type=transaction_type,
            amount=amount1,
            balance_before=balance_before1,
            balance_after=balance_after1,
            description=description1
        )
        
        date2 = "12-06-1996 00:00:00"
        wallet2 = "test_wallet_2"
        amount2 = 50
        balance_before2 = 90
        balance_after2 = 40
        description2 = "test_description_2"
        entry2 = "12-06-1996 00:00:00,test_wallet_2,deduction,50,test_description_2,90,40\n"
        AccountTransactionHandler._queue_transaction(
            date=date2,
            wallet=wallet2,
            transaction_type=transaction_type,
            amount=amount2,
            balance_before=balance_before2,
            balance_after=balance_after2,
            description=description2
        )

        self.assertTrue(AccountTransactionHandler._insert_queued_transactions(self.transaction_filename))
        self.assertListEqual(AccountTransactionHandler._transactions, [])
        with open(self.transaction_filename, "r") as file:
            rows = file.readlines()
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[1], entry1)
            self.assertEqual(rows[2], entry2)

    def test_init_transactions_file_create(self):
        """Transactions file is created if it doesn't exist"""
        os.remove(self.transaction_filename)
        self.assertFalse(os.path.exists(self.transaction_filename))
        self.assertTrue(AccountTransactionHandler._init_transactions_file(self.transaction_filename))
        self.assertTrue(os.path.exists(self.transaction_filename))
        with open(self.transaction_filename, "r") as file:
            content = file.read()
            self.assertEqual(content, AccountTransactionHandler.headers)
    
    def test_init_transactions_file_already_exists(self):
        """Do nothing and return True if the transaction file already exists"""
        self.assertTrue(os.path.exists(self.transaction_filename))
        self.assertFalse(AccountTransactionHandler._init_transactions_file(self.transaction_filename))
        self.assertTrue(os.path.exists(self.transaction_filename))
        with open(self.transaction_filename, "r") as file:
            content = file.read()
            self.assertEqual(content, AccountTransactionHandler.headers)

    

if __name__ == "__main__":
    unittest.main(buffer=True)
