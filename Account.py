from __future__ import annotations
from typing import List
from Wallet import Wallet
import json
import os


class Account():
    def __init__(self, owner: str):
        self.wallet_name = "test_empty_wallet.json"
        self.owner: str = owner
        self.wallets: List[Wallet] = []

        self.__init_wallets_file()

    
    def __init_wallets_file(self) -> None:
        """Makes sure to load the wallets file or create it if it doesn't exist"""
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