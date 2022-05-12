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

        wallet_exists = os.path.exists(self.wallet_name)
        
        if wallet_exists:
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
        """Adds a new wallet to your wallets"""

        self.wallets.append(new_wallet)

    def delete_wallet(self, name: str):
        """Delete an existing wallet from your wallets"""
    
        try:
            wallet_to_delete = self.get_wallet(name)
        except:
            print(f'Wallet {name} could not be found. Please try again.')
            raise
        else:
            self.wallets.remove(wallet_to_delete)