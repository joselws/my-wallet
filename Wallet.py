import json
from typing import List

class Wallet():
    def __init__(self):
        self.__init_wallets()
        self.percents = self.__init_percents()

    def __init_wallets(self):
        # Get the wallets data from the json file, or create it if it doesn't exist
        filename = "test_wallet.json"
        try:
            with open(filename) as file:
                json_contents = file.read()
                wallets = json.loads(json_contents)

                # Set the a class attribute and value for each wallet stored
                for wallet, balance in wallets.items():
                    setattr(self, wallet, balance)

        except FileNotFoundError:
            print("Couldn't find your wallet, perhaps it doesn't exist yet?")
            print("Creating an empty wallet...")
            with open(filename, 'x') as file
            print("Proceed further by creating a wallet using the create_wallet method.")

    def __init_percents(self) -> dict:
        # Get the percents data from the json file, or create it if it doesn't exist
        filename = "test_percents.json"
        try:
            with open(filename) as file:
                json_contents = file.read()
                percents = json.loads(json_contents)
            return percents

        except FileNotFoundError:
            with open(filename, 'x') as file
            return {}

    def create_wallets(self, wallets: List[str] | str):
        """
        Creates a new wallet. You need to provide the following parameters in this order:
        wallets (List[str] | str): List that contains each wallet's name as a string,
            or a single string name
        """

        if type(wallets) is not list or type(wallets) is not str:
            raise TypeError('You need to provide a list of strings or a string.')

        new_wallets = []

        if type(wallets) is list:
            for wallet in wallets:
                if type(wallet) is not str:
                    raise TypeError('The elements of the list need to be strings, please try again.')
                new_wallets.append(wallet)
        else:
            new_wallets.append(wallets)
        
        for wallet in new_wallets:
            setattr(self, wallet)
            self.percents[wallet] = 0

    def delete_wallet(self, wallets: List[str] | str):
        """
        Deletes a wallet (or wallets)
        wallets(List[str] | str): List of strings of wallet names you wish to delete,
            or a single string with the name of the wallet you wish to delete
        """

        if type(wallets) is not list or type(wallets) is not str:
            raise TypeError('You need to provide a list of strings or a string.')

        wallets_to_delete = []

        if type(wallets) is list:
            for wallet in wallets:
                if type(wallet) is not str:
                    raise TypeError('TypeError: The elements of the list need to be strings.')
                if not hasattr(self, wallet):
                    raise AttributeError(f"AttributeError: Couldn't find the wallet {wallet}.")
                wallets_to_delete.append(wallet)
        else:
            if not hasattr(self, wallet):
                raise AttributeError(f"AttributeError: Couldn't find the wallet {wallet}.")
            wallets_to_delete.append(wallets)
        
        for wallet in wallets_to_delete:
            delattr(self, wallet)
            del self.percent[wallet]
            print(f"Wallet {wallet} deleted.")

    def check_percentage(self) -> bool:
        """Returns True if the sum of all wallet percentages is 100"""
        if sum(self.percents.values()) == 100:
            return True
        else:
            return False

    def set_percentages(self):
        """"""
        pass

    def print_wallets(self):
        """Displays on screen all available wallets"""
        pass