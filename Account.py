import json
from typing import List
from Wallet import Wallet


class Account():
    def __init__(self, owner):
        self.__filename = "test_empty_wallet.json"
        self.owner = owner
        self.wallets = []