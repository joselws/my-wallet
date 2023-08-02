import unittest
from TransactionHistory import TransactionHistory
from Transaction import Transaction
from datetime import datetime


TEST_TRANSACTIONS_FILENAME = "test_transactions.csv"


class TestTransactionHistory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_TRANSACTIONS_FILENAME, "w") as file:
            file.write("date,wallet,transaction_type,amount,description,balance_before,balance_after\n")
            file.write("01-05-2023 00:00:00,main,deduction,60,test description 1,3,0\n")
            file.write("12-05-2023 00:00:00,emergencies,deduction,50,test description 2,3,0\n")
            file.write("20-05-2023 00:00:00,charity,deduction,40,test description 3,3,0\n")
            file.write("03-06-2023 00:00:00,main,deduction,30,test description 4,3,0\n")
            file.write("10-06-2023 00:00:00,charity,deduction,20,test description 5,3,0\n")
            file.write("02-07-2023 00:00:00,main,deduction,10,test description 6,3,0\n")

    @classmethod
    def tearDownClass(cls):
        with open(TEST_TRANSACTIONS_FILENAME, "w") as file:
            file.write("date,wallet,transaction_type,amount,description,balance_before,balance_after\n")

    def setUp(self):
        self.th = TransactionHistory(TEST_TRANSACTIONS_FILENAME)

    def test_load_transactions(self) -> None:
        """Transactions are loaded successfully in transactions attribute"""
        self.th.load_transactions()
        self.assertEqual(len(self.th.transactions), 6)

    def test_query_all(self) -> None:
        """Get all transactions by default"""
        self.assertTrue(self.th.query())
        self.assertEqual(len(self.th.queried_transactions), 6)

    def test_query_by_wallet(self) -> None:
        """Get respective transactions by wallet"""
        wallet_name = "main"
        self.assertTrue(self.th.query(wallet=wallet_name))
        self.assertEqual(len(self.th.queried_transactions), 3)
        self.assertTrue(
            all(transaction.wallet == wallet_name for transaction in self.th.queried_transactions)
        )

    def test_query_by_date(self) -> None:
        """Get respective transactions by date"""
        from_date = datetime(year=2023, month=6, day=1)
        to_date = datetime(year=2023, month=6, day=30, hour=23)
        self.assertTrue(self.th.query(from_date="01-06-2023", to_date="30-06-2023"))
        self.assertEqual(len(self.th.queried_transactions), 2)
        self.assertTrue(
            all(
                from_date <= transaction.date <= to_date 
                for transaction 
                in self.th.queried_transactions
            )
        )

    def test_query_by_from_date(self) -> None:
        """Get all transactions between from_date and today"""
        from_date = datetime(year=2023, month=6, day=1)
        to_date = datetime.now()
        self.assertTrue(self.th.query(from_date="01-06-2023"))
        self.assertEqual(len(self.th.queried_transactions), 3)
        self.assertTrue(
            all(
                from_date <= transaction.date <= to_date 
                for transaction 
                in self.th.queried_transactions
            )
        )

    def test_query_by_date_and_wallet(self) -> None:
        """Get all transactions between date ranges and wallet"""
        from_date = datetime(year=2023, month=5, day=1)
        to_date = datetime(year=2023, month=6, day=30)
        wallet_name = "main"
        self.assertTrue(self.th.query(from_date="01-05-2023", to_date="30-06-2023", wallet=wallet_name))
        self.assertEqual(len(self.th.queried_transactions), 2)
        self.assertTrue(
            all(
                from_date <= transaction.date <= to_date 
                for transaction 
                in self.th.queried_transactions
            )
        )
        self.assertTrue(
            all(transaction.wallet == wallet_name for transaction in self.th.queried_transactions)
        )

    def test_query_invalid_wallet(self) -> None:
        """Return empty list when no transactions are found"""
        self.assertFalse(self.th.query(wallet="invalid_wallet_name"))
        self.assertEqual(len(self.th.queried_transactions), 0)

    def test_query_invalid_wallet(self) -> None:
        """Return empty list when no transactions are found by date"""
        self.assertFalse(self.th.query(from_date="01-01-2022", to_date="01-02-2022"))
        self.assertEqual(len(self.th.queried_transactions), 0)

    def test_total_transactions_balance(self) -> None:
        """Returns the correct sum of balances of queried transactions"""
        self.th.query(wallet="main")
        self.assertEqual(self.th.queried_balance(), 100)

    def test_parse_transaction_entry(self) -> None:
        """Convert transaction dictionaries into Transaction objects"""
        transaction_dict = {
            "date": "12-06-1995 00:00:00",
            "wallet": "main",
            "transaction_type": "deduction",
            "amount": 50,
            "description": "test transaction",
            "balance_before": 200,
            "balance_after": 150
        }
        transaction = self.th._parse_transaction_entry(transaction_dict)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.date, datetime(year=1995, month=6, day=12))
        self.assertEqual(transaction.wallet, "main")
        self.assertEqual(transaction.transaction_type, "deduction")
        self.assertEqual(transaction.amount, 50)
        self.assertEqual(transaction.description, "test transaction")
        self.assertEqual(transaction.balance_before, 200)
        self.assertEqual(transaction.balance_after, 150)


if __name__ == '__main__':
    if TransactionHistory(TEST_TRANSACTIONS_FILENAME).filename == "test_transactions.csv":
        unittest.main(buffer=True)
    else:
        print("You're not using your test transactions file!")
