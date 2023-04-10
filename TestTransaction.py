import unittest
from Transaction import Transaction
from datetime import datetime


class TestTransaction(unittest.TestCase):

    def test_transaction_correctly_created(self):
        transaction = Transaction(
            date=datetime(1995, 6, 12, 0, 0, 0),
            wallet_name="main",
            transaction_type="deduction",
            amount=200,
            description="test transaction",
            balance_before=500,
            balance_after=300
        )
        self.assertEqual(transaction.date, datetime(1995, 6, 12, 0, 0, 0))
        self.assertEqual(transaction.wallet_name, "main")
        self.assertEqual(transaction.transaction_type, "deduction")
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.description, "test transaction")
        self.assertEqual(transaction.balance_before, 500)
        self.assertEqual(transaction.balance_after, 300)


if __name__ == "__main__":
    unittest.main()
