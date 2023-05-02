from datetime import datetime
from Transaction import Transaction, TransactionType
import csv


class TransactionHistory:
    
    # class attributes
    transactions_filename = "test_transactions.csv"

    def __init__(self):
        self.transactions = []
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

        args:
            None

        Returns: int indicating whether the operation was successful or not:
            0: if operation was successful
            1: if FileNotFoundError is raised locating transactions file
            2: if there was an error parsing the data from a transaction entry
        """

        try:
            self.transactions.clear()
            with open(self.transactions_filename, "r", newline="") as csvfile:
                transaction_entries = csv.DictReader(csvfile)
                transactions = [
                    self._parse_transaction_entry(row) 
                    for row 
                    in transaction_entries
                ]
                if any(transaction is None for transaction in transactions):
                    return 2
                self.transactions.extend(transactions)
        except FileNotFoundError:
            print(f"File {self.transactions_filename} not found")
            return 1
        else:
            print("Transactions data loaded")
            return 0
        
    def _parse_transaction_entry(self, transaction_entry: dict) -> Transaction:
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
            print(f"Error {error} with a transaction attribute type {transaction_entry}")
            return None
        else:
            return transaction
        
    @classmethod
    def insert_new_transaction(
        cls,
        date: datetime,
        wallet: str,
        transaction_type: TransactionType,
        amount: int,
        balance_before: int,
        balance_after: int,
        description: str = "no_description"
    ) -> bool:
        
        with open(cls.transactions_filename, "a") as file:
            file.write(f"{date},{wallet},{transaction_type},{amount},{description},{balance_before},{balance_after}\n")
