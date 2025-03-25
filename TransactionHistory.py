from datetime import datetime
from Transaction import Transaction, TransactionType
import csv


class TransactionHistory:
    

    def __init__(self, transactions_filename: str):
        """
        You can provide either the name of the transactions filename
        or use acc.get_transactions_filename()
        """
        self.transactions = []
        self.queried_transactions = []
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
        self.filename = transactions_filename

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
            with open(self.filename, "r", newline="") as csvfile:
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
            print(f"File {self.filename} not found")
            return 1
        else:
            print("Transactions data loaded")
            return 0
        
    def _parse_transaction_entry(self, transaction_entry: dict) -> Transaction:
        """
        Return a Transaction object from a transaction entry in dict data
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
        
    def query(self, from_date: str = None, to_date: str = None, wallet: str = None) -> bool:
        """
        Query the transactions file given date range and/or wallet name

        args:
            from_date (Optional): date in day-month-year format. No upper boundary by default
            to_date (Optional): date in day-month-year format. No lower boundary by default
            wallet (Optional): name of a given wallet. Gets transactions from all wallets by default

        returns:
            True if the query brought results.
            False if there are no matches for the query
        """

        self.queried_transactions.clear()
        self.load_transactions()

        if not from_date:
            from_date = datetime.fromtimestamp(0)
        else:
            from_date = f"{from_date} 00:00:00"
            from_date = datetime.strptime(from_date, self.date_format)
        
        if not to_date:
            to_date = datetime.now()
        else:
            to_date = f"{to_date} 23:59:59"
            to_date = datetime.strptime(to_date, self.date_format)

        filtered_transactions = []
        for transaction in self.transactions:
            if from_date <= transaction.date <= to_date:
                filtered_transactions.append(transaction)
        if wallet:
            filtered_transactions = [transaction for transaction in filtered_transactions if transaction.wallet == wallet]

        if not filtered_transactions:
            print("No query data to show")
            return False
        
        self.queried_transactions.extend(filtered_transactions)
        self.show_queried_transactions()
        self.show_aggregated_transactions()
        print(f"Total transaction amount: {self.queried_balance()}")
        print(f"Number of transactions: {len(self.queried_transactions)}")
        return True

        
    def queried_balance(self) -> int:
        """
        Return the sum of all amount values of the transactions queried
        """

        return sum([transaction.amount for transaction in self.queried_transactions])
        
    def show_queried_transactions(self) -> None:
        """
        Prints the queried transactions
        """

        for transaction in self.queried_transactions:
            print(transaction)

    def show_aggregated_transactions(self) -> None:
        """
        Prints the aggregated transactions
        """

        wallet_statistics = {}
        for transaction in self.queried_transactions:
            if transaction.wallet not in wallet_statistics:
                wallet_statistics[transaction.wallet] = {
                    "total": 0,
                    "transactions": 0
                }
            wallet_statistics[transaction.wallet]["total"] += transaction.amount
            wallet_statistics[transaction.wallet]["transactions"] += 1
        
        for wallet, stats in wallet_statistics.items():
            print(f"{wallet}: ${stats['total']} ({stats['transactions']} transactions)")
