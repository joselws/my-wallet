import unittest
from Transaction import Transaction, TransactionType
from datetime import datetime


class TestDeductTransaction(unittest.TestCase):

    def test_deduct_transaction_correctly_created(self):
        transaction = Transaction(
            date=datetime(1995, 6, 12, 0, 0, 0),
            wallet="main",
            transaction_type=TransactionType.DEDUCTION.value,
            amount=200,
            description="test deduct transaction",
            balance_before=500,
            balance_after=300
        )
        self.assertEqual(transaction.date, datetime(1995, 6, 12, 0, 0, 0))
        self.assertEqual(transaction.wallet, "main")
        self.assertEqual(transaction.transaction_type, "deduction")
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.description, "test deduct transaction")
        self.assertEqual(transaction.balance_before, 500)
        self.assertEqual(transaction.balance_after, 300)


if __name__ == "__main__":
    unittest.main()
