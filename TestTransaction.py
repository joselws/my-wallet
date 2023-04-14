import unittest
from Transaction import DeductTransaction, TransferTransaction, TransactionType
from datetime import datetime


class TestDeductTransaction(unittest.TestCase):

    def test_deduct_transaction_correctly_created(self):
        transaction = DeductTransaction(
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


class TestTransferTransaction(unittest.TestCase):

    def test_transfer_transaction_correctly_created(self):
        transaction = TransferTransaction(
            date=datetime(1995, 6, 12, 0, 0, 0),
            from_wallet_name="main",
            to_wallet_name="charity",
            transaction_type=TransactionType.TRANSFER.value,
            amount=200,
            description="test transfer transaction",
            from_wallet_balance_before=500,
            from_wallet_balance_after=300,
            to_wallet_balance_before=1000,
            to_wallet_balance_after=1200,
        )
        self.assertEqual(transaction.date, datetime(1995, 6, 12, 0, 0, 0))
        self.assertEqual(transaction.from_wallet_name, "main")
        self.assertEqual(transaction.to_wallet_name, "charity")
        self.assertEqual(transaction.transaction_type, "transfer")
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.description, "test transfer transaction")
        self.assertEqual(transaction.from_wallet_balance_before, 500)
        self.assertEqual(transaction.from_wallet_balance_after, 300)
        self.assertEqual(transaction.to_wallet_balance_before, 1000)
        self.assertEqual(transaction.to_wallet_balance_after, 1200)

    


if __name__ == "__main__":
    unittest.main()
