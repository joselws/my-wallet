from dataclasses import dataclass
from datetime import datetime
import csv

@dataclass(frozen=True)
class Transaction:
    date: datetime
    wallet: str
    transaction_type: str
    amount: int
    description: str
    balance_before: int
    balance_after: int


class TransactionHistory:
    
    def __init__(self):
        self.transactions = []
        self.transactions_filename = "transactions.csv"
        self.date_format = "%d-%m-%Y %H:%M:%S"
        self.headers = [
            "date",
            "wallet",
            "transaction_type",
            "amount",
            "description",
            "balance_before",
            "balance_after"
        ]

    def load_transactions(self) -> int:
        """
        Read the contents of the transactions file,
        parses the columns of each member,
        creates a transaction object for each entry,
        and appends it to self.transactions list attribute
        """

        try:
            self.transactions.clear()
            with open(self.transactions_filename, "r", newline="") as csvfile:
                transaction_entries = csv.DictReader(csvfile)
                for row in transaction_entries:
                    if not (transaction := self._convert_into_object(row)):
                        return 2
                    self.transactions.append(transaction)
        except FileNotFoundError:
            print(f"File {self.transactions_filename} not found")
            return 1
        else:
            print("Transactions data loaded")
            return 0
        
    def _convert_into_object(self, transaction_entry: dict) -> Transaction:
        """
        
        """

        try:
            transaction = Transaction(
                date=datetime.strptime(transaction_entry["date"], self.date_format),
                wallet=transaction_entry["wallet"],
                transaction_type=transaction_entry["transaction_type"],
                amount=int(transaction_entry["amount"]),
                description=transaction_entry["description"],
                balance_before=int(transaction_entry["balance_before"]),
                balance_after=int(transaction_entry["balance_after"])
            )
        except ValueError as error:
            print(f"Error {error} with a transaction atribute type {transaction_entry}")
            return None
        else:
            return transaction
