import os

class AccountTransactionHandler:
    """
    Handles all the logic about initializing and saving transaction entries
    from Account transaction type movements

    This class is never instantiated, and all its methods are classmethods,
    so its methods are called directly from the class

    You should never have to touch and call this class directly, it's made only
    for use within the Account class internal functionalities
    """

    # class attributes
    _transactions = []
    headers = "date,wallet,transaction_type,amount,description,balance_before,balance_after\n"

    @classmethod
    def _queue_transaction(
        cls, 
        date: str,
        wallet: str,
        transaction_type: str,
        amount: int,
        balance_before: int,
        balance_after: int,
        description: str = "no_description"
    ) -> None:
        """
        Queue a transaction entry into the list

        args:
            date(str): dd-mm-yyyy hh:mm:ss 
            wallet(str): name of the wallet
            transaction_type(str): TransactionType type value
            amount(int): amount of money for transaction type
            balance_before(int): balance before transaction type occurs
            balance_after(int): balance after transaction type occurs
            description(str, Optional): transaction type movement description

        returns: None
        """
        entry = f"{date},{wallet},{transaction_type},{amount},{description},{balance_before},{balance_after}\n"
        cls._transactions.append(entry)


    @classmethod
    def _insert_queued_transactions(cls, transactions_filename: str) -> bool:
        """
        Put all the transaction entries in queue in the transactions file

        args:
            transactions_filename(str): name of the transaction file

        returns:
            bool: True if the file is found and process completes without errors
                  False if the transctions file is not found
        """
        if not os.path.exists(transactions_filename):
            print(f"Error. File {transactions_filename} was not found.")
            return False
        with open(transactions_filename, "a") as file:
            for transaction in cls._transactions:
                file.write(transaction)
        cls._transactions.clear()
        return True
            

    @classmethod
    def _show_queued_transactions(cls) -> bool:
        """
        Shows the queued transactions

        args: None

        returns:
            True if there are queued transactions to show
            False if there are none
        """
        if cls._transactions:
            for transaction in cls._transactions:
                print(transaction)
            return True
        else:
            print("There are no transactions in queue.")
            return False
        
    
    @classmethod
    def _empty_queued_transactions(cls) -> None:
        """
        Empty all the queued transactions in the list
        """
        cls._transactions.clear()
        

    @classmethod
    def _init_transactions_file(cls, transaction_filename: str) -> bool:
        """
        Make sure to create the transactions.csv file with its proper headers
        if it doesn't exist yet

        args:
            transactions_filename(str): name of the transaction file
        
        returns:
            True if it didn't exist and was successfully created
            False if the transaction file already exists
        """

        if os.path.exists(transaction_filename):
            return False
        else:
            with open(transaction_filename, "w") as file:
                file.write(cls.headers)
            return True
