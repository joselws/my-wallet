from __future__ import annotations
from typing import List, Tuple
from Wallet import Wallet
from datetime import datetime
from Transaction import TransactionType
from AccountTransactionHandler import AccountTransactionHandler
import json
import os


class Account():
    """
    This single account entity provides the functionality for managing
    all the wallets for an owner. 
    """

    def __init__(self, wallet_name: str = "test_wallet.json"):
        self.__wallet_name = wallet_name
        if wallet_name in ["test_wallet.json", "test_empty_wallet.json"]:
            self.__transactions_name = "test_transactions.csv"
        else:
            self.__transactions_name = "transactions.csv"
        self.wallets: List[Wallet] = []
        self.savings_wallets: List[str] = [
            'emergencies',
            'savings',
            'investing',
            'binance-btc',
            'travels',
        ]

        self.__init_wallets_file()
        AccountTransactionHandler._init_transactions_file(
            self.get_transactions_file_name()
        )


    def get_wallet_name(self) -> str:
        """Returns the name of the wallet JSON file"""
        return self.__wallet_name
    
    def get_transactions_file_name(self) -> str:
        """Returns the name of the transactions csv file"""
        return self.__transactions_name
    
    def __init_wallets_file(self) -> None:
        """
        Makes sure to load the wallets file or create it if it doesn't exist.
        Internal use only
        """

        if os.path.exists(self.__wallet_name):
            with open(self.__wallet_name) as file:
                json_content = file.read()
                if not len(json_content):
                    self.add_wallet('main')
                    self.save()
                    print('Wallet created.')
                else:
                    wallets: List = json.loads(json_content)
                    for wallet_dict in wallets:
                        wallet = Wallet(**wallet_dict)
                        self.wallets.append(wallet)
        else:
            self.add_wallet('main')
            with open(self.__wallet_name, 'w') as file:
                self.save()
                print('Wallet created.')


    def get_wallet(self, name: str) -> Wallet:
        """
        Returns an existing wallet object of the specified name
        """

        for wallet in self.wallets:
            if name == wallet.name:
                return wallet

    def add_wallet(self, name: str, balance: int = 0, percent: int = 0, cap: int = 0) -> None:
        """
        Adds a new wallet to your wallets provided a name
        balance (optional) is the current amount of money the wallet holds
        percent (optional) current percent data the wallet has
        cap (optional) maximum amount of money the wallet is allowed to have
        """

        __wallet_names = [wallet.name for wallet in self.wallets]
        if name in __wallet_names:
            print(f'Wallet {name} already exists. Please try again.')
            return
        else:
            if self.valid_number(balance) and self.valid_number(percent) and self.valid_number(cap):
                new_wallet = Wallet(name, balance, percent, cap)
                if new_wallet.cap and new_wallet.balance > new_wallet.cap:
                    print('Error: Balance value must not be greater than Cap')
                    return
                self.wallets.append(new_wallet)
                print(f"Wallet {new_wallet.name} created.")
            else:
                print(f'Bad input, please try again.')

    def delete_wallet(self, name: str):
        """
        Delete an existing wallet from your wallets
        """

        if name == 'main':
            print('Main wallet should not be deleted.')
            return

        wallet_to_delete = self.get_wallet(name)
        if not wallet_to_delete:
            print(f'Wallet {name} could not be found. Please try again.')
        else:
            self.transfer(name, 'main')
            self.wallets.remove(wallet_to_delete)
            print(f"Wallet {name} deleted.")

    def correct_percent(self) -> bool:
        """
        Returns true if the sum of the percentages of all wallets is 100
        Return false otherwise
        """

        percents = [wallet.percent for wallet in self.wallets]
        if not percents:
            return False
        elif sum(percents) == 100:
            return True
        else:
            return False

    def valid_number(self, *args: Tuple[int]) -> bool:
        """
        Returns true if the given numbers in args are positive integers
        Otherwise returns False
        """

        for value in args:
            if type(value) is not int or value < 0:
                return False 
        return True

    def transfer(self, _from: str, to: str, amount: int = None) -> None:
        """
        Transfer a desired amount of money from one wallet to another
        """

        from_wallet = self.get_wallet(_from)
        to_wallet = self.get_wallet(to)
        if not from_wallet or not to_wallet:
            print('Please insert valid wallet names.')
            return

        if amount is not None:
            if not self.valid_number(amount):
                print('Only positive integers are permitted. Try again.')
                return
            if amount > from_wallet.balance:
                print('Money to transfer surpasses wallet amount. Please try again.')
                return

            print(f"Balance of {from_wallet.name} changed from {from_wallet.balance} ", end="")
            from_wallet -= amount
            print(f"to {from_wallet.balance}")
            print(f"Balance of {to_wallet.name} changed from {to_wallet.balance} ", end="")
            to_wallet += amount
            print(f"to {to_wallet.balance}\n")
            self.correct_cap(to_wallet)
        
        # Transfer all the money if amount is None
        else:
            amount = from_wallet.balance
            print(f"Balance of {from_wallet.name} changed from {from_wallet.balance} ", end="")
            from_wallet -= amount
            print(f"to {from_wallet.balance}")
            print(f"Balance of {to_wallet.name} changed from {to_wallet.balance} ", end="")
            to_wallet += amount
            print(f"to {to_wallet.balance}")

    def total(self) -> str:
        """
        Outputs the total amount of money available
        i.e. the sum of the balance of all wallets
        """

        total = sum([wallet.balance for wallet in self.wallets])
        return f'${total}'

    def total_except(self, *names: Tuple[str]) -> str:
        """
        Takes as arguments as many existing wallet names,
        returns the sum of all balances except those whose names were given
        """
        except_wallets = [self.get_wallet(wallet_name) for wallet_name in names]
        
        if any(wallet is None for wallet in except_wallets):
            print('One of the wallet names provided does not exist.')
            return None
        
        total = sum([wallet.balance for wallet in self.wallets if wallet not in except_wallets])
        return f"${total}"

    def save(self) -> None:
        """Save changes to json wallet file"""
        wallets: List = [wallet.__dict__ for wallet in self.wallets]
        wallets_json = json.dumps(wallets)
        with open(self.__wallet_name, 'w') as file:
            file.write(wallets_json)
            AccountTransactionHandler._insert_queued_transactions(self.get_transactions_file_name())
            print('Saved Changes.')

    def deduct(self, name: str, description: str = None, amount: int = None):
        """
        Deduct the desired amount of money from a wallet
        """

        wallet = self.get_wallet(name)
        if not wallet:
            print('No wallet under that name could be found.')
            return

        if not wallet.balance:
            print("No available balance to deduct from.")
            return
        
        balance_before = wallet.balance
        date = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
        if not description:
            description = "no_description"

        if amount is not None:
            if not self.valid_number(amount) or amount > wallet.balance:
                print('Error with the amount input, please try again.')
                return
            else:
                balance_after = wallet.balance - amount
                print(f"Wallet balance changed from {wallet.balance} ", end="")
                wallet.balance -= amount
                print(f"to {wallet.balance}")
        else:
            print(f"Wallet {wallet.name} balance {wallet.balance} set to 0")
            amount = wallet.balance
            balance_after = 0
            wallet.balance = 0

        AccountTransactionHandler._queue_transaction(
            date,
            name,
            TransactionType.DEDUCTION.value,
            amount,
            balance_before, 
            balance_after,
            f'"{description}"', 
        )

    def percents(self) -> None:
        """Show existing percents of each wallet"""

        for wallet in self.wallets:
            if wallet.percent > 0:
                print(f"{wallet.name}: {wallet.percent}%")

    def set_percents(self) -> None:
        """Show current wallets percents and prompts user to set them"""

        print("Showing current wallet percentages")
        for wallet in self.wallets:
            if wallet.name != 'main':
                print(f'Wallet {wallet.name}: {wallet.percent}%')
        print('')   # newline

        wallets = [wallet.name for wallet in self.wallets if wallet.name != 'main']
        wallets_dict = {}

        for wallet in wallets:
            new_percent = input(f'Set percent of Wallet {wallet}: ')
            try:
                new_percent = int(new_percent)
            except ValueError:
                print('Not valid number format, please try again.')
                return
            else:
                if self.valid_number(new_percent) and new_percent <= 100 :
                    wallets_dict[wallet] = new_percent
                else:
                    print('Not a valid number format, please try again.')
                    return
            
        self.calc_percents(wallets_dict)

    def calc_percents(self, percents: dict) -> None:
        """Calculates the main wallet percent and set all percents on wallets"""
        
        percents_sum = sum([percent for percent in percents.values()])
        if percents_sum <= 100:
            main = self.get_wallet('main')
            main.percent = 100 - percents_sum

            for name, percent in percents.items():
                self.get_wallet(name).percent = percent

            if self.correct_percent():
                print('Percent values correctly set on wallets.\n')
            else:
                print('Unknown error, please try again!\n')

        else:
            print('Percents not correctly set, please try again.\n')

    def correct_cap(self, wallet: Wallet) -> None:
        """
        Checks whether the balance of the wallet surpasses its cap,
        and if so, perform the necessary adjustments and calculations
        """

        if not (main := self.get_wallet('main')):
            self.add_wallet('main')
            main = self.get_wallet('main')
            print('main Wallet created.')

        if wallet.cap and wallet.balance > wallet.cap:
            extra_money = wallet.balance - wallet.cap
            wallet.balance = wallet.cap

            main.balance += extra_money
            wallet.percent = 0

            print(f"Wallet {wallet.name} balance set to {wallet.cap} and transfering {extra_money} to main")
            print(f'Wallet {wallet.name} with balance of {wallet.balance} surpassed its cap of {wallet.cap} by {extra_money}')
            print(f"Transfering {main.balance} to main\n")
        
    def deposit(self, amount: int) -> None:
        """
        Deposits money and distributes it among all wallets
        according to their percent data attribute
        all percent values must add up to 100
        """

        if not self.valid_number(amount):
            print('Not a valid number format.')
            return

        if not self.correct_percent():
            print('Percent values among wallets do not add up to 100, please set them and try again.')
            return
        
        # calculate the respective amount of money to all wallets except main
        wallets_part = {}
        wallets = [wallet for wallet in self.wallets if wallet.percent > 0]
        for wallet in wallets:
            if wallet.name != 'main':
                part = (amount * wallet.percent) // 100
                wallets_part[wallet.name] = part

        # transfer the calculated money to each wallet
        for name, part_money in wallets_part.items():
            wallet = self.get_wallet(name)
            print(f'Depositing {part_money} to {name} (${wallet.balance}). ', end="")
            wallet.balance += part_money
            print(f"Now ${wallet.balance}")
            amount -= part_money
            self.correct_cap(wallet)

        # transfer the remaining amount of money to main
        main = self.get_wallet('main')
        print(f'Depositing {amount} to main (${main.balance}). ', end="")
        main += amount
        print(f"Now ${main.balance}\n")

    def check_wallets(self) -> None:
        """Show all information of all wallets"""
        
        for wallet in self.wallets:
            print(f'Name: {wallet.name}')
            print(f'Balance: ${wallet.balance}')
            print(f'Percent: {wallet.percent}%')
            print(f'Cap: ${wallet.cap}')
            
            if wallet.cap:
                print(f"${(wallet.cap - wallet.balance)} more to reach the cap\n")
            else:
                print("No cap limit\n")

    def add(self, name: str, amount: int) -> None:
        """Adds an amount of money to a wallet"""
        
        wallet = self.get_wallet(name)
        if not wallet:
            print(f'Wallet {name} could not be found.')
            return
        else:
            if self.valid_number(amount):
                print(f"Wallet {wallet.name} from {wallet.balance} ", end="")
                wallet += amount
                print(f"to {wallet.balance}")
                self.correct_cap(wallet)
            else:
                print('Not a valid number format.')

    def edit(self, wallet_name: str, name: str, balance: int, percent: int, cap: int) -> None:
        """
        edit an existing wallet
        
        args:
            - wallet (str): Name of the wallet you want to edit
            - name (str): New name you want to put to your wallet
            - balance, percent, cap (int): respective values
        """

        if wallet_name == 'main':
            print("Can't edit main.")
            return
            
        if current_wallet := self.get_wallet(wallet_name):
            invalid_names = [wallet.name for wallet in self.wallets if wallet.name != current_wallet.name]
            if name not in invalid_names and self.valid_number(balance, percent, cap):
                current_wallet.name = name
                current_wallet.balance = balance
                current_wallet.percent = percent
                current_wallet.cap = cap
                self.show(current_wallet.name)
        else:
            print(f"Wallet {wallet_name} couldn't be found.")

    def usable(self) -> str:
        """
        Returns the total amount of money you may use 
        (the money not in savings wallets)
        """

        usable_money = sum([wallet.balance for wallet in self.wallets if wallet.name not in self.savings_wallets])
        return f'${usable_money}'

    def non_usable(self) -> str:
        """
        Returns the total amount of money you should NOT use 
        (the money in savings wallets)
        """

        non_usable_money = sum([wallet.balance for wallet in self.wallets if wallet.name in self.savings_wallets])
        return f'${non_usable_money}'

    def total_on(self, *names: Tuple[str]) -> str:
        """
        Returns the sum of the balance of all specified wallets
        
        *names: n string wallet names
        """

        total = 0
        for name in names:
            if wallet := self.get_wallet(name):
                total += wallet.balance
            else:
                print(f"Wallet {name} couldn't be found. Please try again.")
                return
        
        return f"${total}" if total else None

    def summary(self) -> None:
        """Prints all relevant information about your account"""

        print(f'Total amount of money {self.total()}')
        print(f'Total usable money {self.usable()}')
        print(f'Total non-usable of money {self.non_usable()}\n')
        self.check_wallets()

    def show(self, name: str):
        """Show all properties of a wallet given its name"""
        
        if wallet := self.get_wallet(name):
            print(f"Name: {wallet.name}")
            print(f"balance: {wallet.balance}")
            print(f"percent: {wallet.percent}")
            print(f"cap: {wallet.cap}\n")
        else:
            print(f"Wallet {name} doesn't exist!")

    @staticmethod
    def show_queued_transactions() -> None:
        """Show all queued transactions."""
        AccountTransactionHandler._show_queued_transactions()

    def rename(self, wallet_name: str, new_name: str) -> None:
        """Renames a wallet"""

        if wallet_name == 'main':
            print("Can't rename the main wallet.")
            return
        
        if (wallet := self.get_wallet(wallet_name)) and not self.get_wallet(new_name):
            print(f"Wallet {wallet.name} changed to {new_name}")
            wallet.name = new_name
        else:
            print(f"Error with wallet names, please try again!")

    def reset(self) -> None:
        """Resets the account to the previous saved state"""

        self.wallets.clear()
        with open(self.__wallet_name) as file:
            json_content = file.read()

        wallets: List = json.loads(json_content)
        for wallet_dict in wallets:
            wallet = Wallet(**wallet_dict)
            self.wallets.append(wallet)

        AccountTransactionHandler._empty_queued_transactions()
        print("Account has been reset.")

    def set_cap(self, name: str, cap: int) -> None:
        """Set the cap attribute of a wallet given its name"""

        if not self.valid_number(cap):
            print('Not a valid cap value, please try again.')
            return

        if name == 'main':
            print("You can't do this operation on the main wallet.")
            return

        if wallet := self.get_wallet(name):
            print(f"Wallet {name} cap of {wallet.cap} changed to {cap}")
            wallet.cap = cap
            self.correct_cap(wallet)
        else:
            print('Wallet not found!')

    def merge(self, wallet_one_name: str, wallet_two_name: str) -> None:
        """Combine wallet two into wallet one if both exist"""

        wallet_one = self.get_wallet(wallet_one_name)
        wallet_two = self.get_wallet(wallet_two_name)

        if not wallet_one or not wallet_two:
            print("Invalid operation. One or both of the wallets couldn't be found.")
            return

        print(f"Combining percent of {wallet_one.percent} to {wallet_two.percent}, now ", end="")
        wallet_one.percent += wallet_two.percent
        print(wallet_one.percent)

        print(f"Combining cap of {wallet_one.cap} to {wallet_two.cap}, now ", end="")
        self.set_cap(wallet_one_name, wallet_one.cap + wallet_two.cap)
        print(wallet_one.cap)

        print(f"Combining balance of {wallet_one.balance} to {wallet_two.balance}, now ", end="")
        self.transfer(wallet_two_name, wallet_one_name)
        print(wallet_one.balance)

        self.delete_wallet(wallet_two_name)
        
    def clear_all(self) -> None:
        """Sets all wallets data to zero"""
        for wallet in self.wallets:
            wallet.percent = wallet.balance = wallet.cap = 0
        print("All wallet values set to zero (0)")

    def clear(self, name: str) -> None:
        """Set all data of a given wallet to zero"""
        
        if wallet := self.get_wallet(name):
            wallet.balance = wallet.percent = wallet.cap = 0
            print(f"Wallet {wallet.name} values set to zero (0).")
        else:
            print(f"Wallet {name} doesn't exist!")

    def wipe(self) -> None:
        """Deletes all wallet data in your account"""
        self.wallets.clear()
        print('All wallet data has been deleted.')

    def help(self):
        """Prints info about the class methods"""
        return help(self)

    def __repr__(self) -> str:
        return f'Account: {[wallet.name for wallet in self.wallets]}'

    def __len__(self) -> int:
        return len(self.wallets)