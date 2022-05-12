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
            with open(self.wallet_name, 'w') as file:
                file.write('[]')
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
    
        try:
            wallet_to_delete = self.get_wallet(name)
        except:
            print(f'Wallet {name} could not be found. Please try again.')
            raise
        else:
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