from __future__ import annotations
from typing import List
from Wallet import Wallet
import json
import os


class Account():
    """
    This single account entity provides the functionality for managing
    all the wallets for an owner. 
    """

    def __init__(self, owner: str):
        self.__wallet_name = "test_wallet.json"
        self.owner: str = owner
        self.wallets: List[Wallet] = []

        self.__init_wallets_file()


    def get_wallet_name(self) -> str:
        """Returns the name of the wallet JSON file"""
        return self.__wallet_name
    
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
        print(f'Wallet {name} not found. Try again.')

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
                self.wallets.append(Wallet(name, balance, percent, cap))
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

    def correct_percent(self) -> bool:
        """
        Returns true if the sum of the percentages of all wallets is 100
        Return false otherwise
        """

        percents = [wallet.percent for wallet in self.wallets if wallet.percent is not None]
        if not percents:
            return False
        elif sum(percents) == 100:
            return True
        else:
            return False

    def valid_number(self, value) -> bool:
        """
        Returns true if the given number is a positive integer
        Otherwise returns False
        """

        if type(value) is int and value >= 0:
            return True
        else:
            return False 

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
            from_wallet -= amount
            to_wallet += amount
        
        # Transfer all the money if amount is None
        else:
            amount = from_wallet.balance
            from_wallet -= amount
            to_wallet += amount

    def total(self) -> str:
        """
        Outputs the total amount of money available
        i.e. the sum of the balance of all wallets
        """

        total = sum([wallet.balance for wallet in self.wallets])
        return f'${total}'

    def save(self) -> None:
        """Save changes to json wallet file"""
        wallets: List = [wallet.__dict__ for wallet in self.wallets]
        wallets_json = json.dumps(wallets)
        with open(self.__wallet_name, 'w') as file:
            file.write(wallets_json)
            print('Saved Changes.')

    def deduct(self, name: str, amount: int = None):
        """
        Deduct the desired amount of money from a wallet
        """

        wallet = self.get_wallet(name)
        if not wallet:
            print('No wallet under that name could be found.')
            return
        else:
            if amount is not None:
                if not self.valid_number(amount) or amount > wallet.balance:
                    print('Error with the amount input, please try again.')
                else:
                    wallet.balance -= amount
            else:
                wallet.balance = 0

    def set_percentages(self) -> None:
        """Show current wallets percents and prompts user to set them"""

        print("Showing current wallet percentages")
        for wallet in self.wallets:
            if wallet.name != 'main':
                print(f'Wallet {wallet.name}: {wallet.percent}%')

        print('')   # newline
        for wallet in self.wallets:
            if wallet.name == 'main':
                continue

            new_percent = input(f'Set percent of Wallet {wallet.name}: ')
            try:
                new_percent = int(new_percent)
            except ValueError:
                print('Not valid number format, please try again.')
                return
            else:
                if self.valid_number(new_percent) and new_percent <= 100 :
                    wallet.percent = new_percent
                else:
                    print('Not a valid number format, please try again.')
            # Set 'main' wallet percent to be the remaining percent to complete 100
            finally:
                percents = sum([wallet.percent for wallet in self.wallets if wallet.name != 'main'])
                if percents < 100:
                    main = self.get_wallet('main')
                    main.percent = 100 - percents
                    print('Percents correctly set.\n')
                else:
                    print('Percents not correctly set, please try again.\n')
    
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
        for wallet in self.wallets:
            if wallet.name != 'main':
                part = (amount * wallet.percent) // 100
                wallets_part[wallet.name] = part

        # transfer the calculated money to each wallet
        for name, part_money in wallets_part.items():
            wallet = self.get_wallet(name)
            print(f'Depositing {part_money} to {name}')
            wallet.balance += part_money
            amount -= part_money

        # transfer the remaining amount of money to main
        main = self.get_wallet('main')
        print(f'Depositing {amount} to main\n')
        main += amount

    def check_wallets(self) -> None:
        """Show all information of all wallets"""
        
        for wallet in self.wallets:
            print(f'Name: {wallet.name}')
            print(f'Balance: ${wallet.balance}')
            print(f'Percent: {wallet.percent}%')
            print(f'Cap: ${wallet.cap}\n')

    def add(self, name: str, amount: int) -> None:
        """Adds an amount of money to a wallet"""
        
        wallet = self.get_wallet(name)
        if not wallet:
            print(f'Wallet {name} could not be found.')
            return
        else:
            if self.valid_number(amount):
                wallet += amount
            else:
                print('Not a valid number format.')

    def reset(self) -> None:
        """Resets the account to the previous saved state"""

        self.wallets.clear()
        with open(self.__wallet_name) as file:
            json_content = file.read()

        wallets: List = json.loads(json_content)
        for wallet_dict in wallets:
            wallet = Wallet(**wallet_dict)
            self.wallets.append(wallet)

    def help(self):
        """Prints info about the class methods"""
        return help(self)

    def __repr__(self) -> str:
        return f'Account: {self.owner}'

    def __len__(self) -> int:
        return len(self.wallets)