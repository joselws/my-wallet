from __future__ import annotations
from typing import List
from Wallet import Wallet
import json
import os


class Account():
    """
    This single account entity provides the functionality for managing
    all the wallets for an owner. 

    Attrs:
    wallet_name[str]: name of the json file that will store the owner's wallet data
    owner[str]: name of the owner of the wallets
    wallets[List[Wallet]]: list that contains all the owner's wallets

    Methods:
    """

    def __init__(self, owner: str):
        self.wallet_name = "test_wallet.json"
        self.owner: str = owner
        self.wallets: List[Wallet] = []

        self.__init_wallets_file()

    
    def __init_wallets_file(self) -> None:
        """
        Makes sure to load the wallets file or create it if it doesn't exist.
        Internal use only
        """

        if os.path.exists(self.wallet_name):
            with open(self.wallet_name) as file:
                json_content = file.read()
                wallets: List = json.loads(json_content)

            for wallet_dict in wallets:
                wallet = Wallet(**wallet_dict)
                self.wallets.append(wallet)
        
        else:
            self.add_wallet(Wallet('main'))
            with open(self.wallet_name, 'w') as file:
                self.save()
                print('Wallet created')

    def get_wallet(self, wallet_name: str) -> Wallet:
        """
        Returns the wallet of the specified name,
        or raises an exception if it is not found
        """

        for wallet in self.wallets:
            if wallet_name == wallet.name:
                return wallet
        raise Exception(f'Wallet {wallet_name} not found. Try again.')

    def add_wallet(self, new_wallet: Wallet) -> None:
        """
        Adds a new wallet to your wallets,
        or raises an exception if the wallet name is repeated
        """

        wallet_names = [wallet.name for wallet in self.wallets]
        if new_wallet.name in wallet_names:
            raise Exception(f'Wallet {new_wallet.name} already exists. Please try again.')
        else:
            self.wallets.append(new_wallet)

    def delete_wallet(self, name: str):
        """
        Delete an existing wallet from your wallets
        or raises an exception if the wallet couldn't be found
        """

        if name == 'main':
            raise Exception('Main wallet should not be deleted')

        try:
            wallet_to_delete = self.get_wallet(name)
        except:
            print(f'Wallet {name} could not be found. Please try again.')
            raise
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

        if type(value) is int and value > 0:
            return True
        else:
            return False 

    def transfer(self, _from: str, to: str, amount: int = None) -> None:
        """
        Transfer a desired amount of money from one wallet to another
        Non-valid numbers and money that surpasses a wallet amount
        raise exceptions
        """

        try:
            from_wallet = self.get_wallet(_from)
            to_wallet = self.get_wallet(to)
        except:
            print('Please insert valid wallet names.')
            raise

        if amount is not None:
            if not self.valid_number(amount):
                raise ValueError('Only positive integers are permitted. Try again.')
            if amount > from_wallet.balance:
                raise Exception('Money to transfer surpasses wallet amount. Please try again.')
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
        with open(self.wallet_name, 'w') as file:
            file.write(wallets_json)
            print('Saved Changes')

    def deduct(self, wallet_name: str, amount: int = None):
        """
        Deduct the desired amount from the wallet
        """

        try:
            wallet = self.get_wallet(wallet_name)
        except:
            print('No wallet under that name could be found.')
            raise
        else:
            if amount is not None:
                if amount > wallet.balance:
                    raise Exception('Error: amount greater than wallet balance.')
                else:
                    wallet.balance -= amount
            else:
                wallet.balance = 0

    def set_percentagees(self) -> None:
        """Show current wallets percents and prompts user to set them"""

        print("Showing current wallet percentages")
        for wallet in self.wallets:
            print(f'Wallet {wallet.name} {wallet.percent}%')

        for wallet in self.wallets:
            new_percent = input(f'Set percent of Wallet {wallet.name}: ')
            try:
                new_percent = int(new_percent)
            except ValueError:
                print('Not valid number format, please try again.')
                raise
            else:
                if self.valid_number(new_percent) and new_percent <= 100 :
                    wallet.percent = new_percent
                else:
                    raise Exception('Not a valid number format, please try again.')
    
    def deposit(self, amount: int) -> None:
        """Deposit money and distribute it among all wallets"""

        if not self.valid_number(amount):
            raise ValueError('Not a valid number format.')
        
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
        print(f'Depositing {amount} to main')
        main += amount