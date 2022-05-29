# My Wallet

This is a Python program used to help you manage your personal finances. Have all the different wallets you need, so you can use them for different financial purposes. For example, you might want a wallet for ***savings*** and another one for ***home***.

You manage one account object under any name, and you call methods of that account object to do all the functionalities providen in this program.

All your data is saved into a JSON file that serves the purpose of a tiny database.

## Quickstart

1. Clone this repo in a folder of your choice

2. Enter your command-line interface program and navigate to this directory

3. Enter the Python interpreter

4. Run

```
>>> from Account import Account
>>> <your_account_name> = Account('<desired_account_name>')
```

For example, `acc = Account('tom')`

5. Use the `help()` function or the `help()` method on the Account object if you need a quick overview of the commands in-session. For example, `help(acc)` or `acc.help()`

## Methods

- `help()`: Display information about the available class methods. Example: `acc.help()`

- `add_wallet(name, balance, percent, cap)`: Add a new wallet to your account. `name` is a `string`, while `balance`, `percent`, and `cap` are `int`s. Example: `acc.add_wallet('home', 150, 20, 30000)`

- `delete_wallet(name)`: Delete an existing wallet given its *name*. `name` is a `string`. Example: `acc.delete_wallet('home')`

- `deposit(amount)`: Transfer a given *amount* of money across all your wallets according to their percentages. Note that the total percent among all wallets must add up to 100. `amount` is an `int`. Example: `acc.deposit(1000)`

- `transfer(_from, to, amount)`: Transfer a given *amount* of money *from* a walllet *to* another. `amount` is an `int`, while `_from` and `to` are `string`s. For example: `acc.transfer('home', 'main', 300)`

- `add(name, amount)`: Adds a given *amount* of money to a wallet given its *name*. `name` is a `string` while `amount` is an `int`. Example: `acc.add('main', 250)`

- `deduct(name, amount)`: Deducts a certain *amount* of money from a wallet given its *name*. `name` is a `string` and `amount` is an `int`. For example: `acc.deduct('main', 500)`

- `total()`: Prints the *total* amount of money from all your wallets. Example: `acc.total()`

- `set_percentages()`: Set the percentage attribute of each wallet. For example: `acc.set_percentages()`

- `check_wallets()`: Prints all information aof all your wallets. Example: `acc.check_wallets()`

- `save()`: Save your changes. Example: `acc.save()`

- `reset()`: Return to the last saved state of your account. Example: `acc.reset()`

- `wipe()`: Deletes all wallets data in your account; you're left with an empty account with no wallets. Example: `acc.wipe()`

- `clear()`: Sets all data in all your wallets to zero. Example: `acc.clear()`

## Tips

- Use `acc.wallets` to print a quick summary of all your wallets.

- Use `len(acc)` to print the number of wallets you have.

## Important

- A wallet called **main** is included by default in all wallets and you cannot delete it unless you do it directly, but you're strongly ***not*** encouraged to do so since this wallet is essential to some of the internal functionalities of the program.

- The functionality of the `cap` data attribute of a Wallet object has not yet been implemented.

- If you find any bugs, please let me know!
