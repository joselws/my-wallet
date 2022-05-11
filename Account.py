from __future__ import annotations
from typing import List
from Wallet import Wallet
import json
import os


class Account():
    def __init__(self, owner: str):
        self.wallet_name = "test_wallet.json"
        self.owner: str = owner
        self.wallets: List[Wallet] = []

        self.__init_wallets_file()

    
    def __init_wallets_file(self) -> None:
        """Makes sure to load the wallets file or create it if it doesn't exist"""
        if os.path.exists(self.wallet_name):
            pass
        else:
            with open(self.wallet_name, 'w') as file:
                pass