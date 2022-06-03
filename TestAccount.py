import json
import os
from Account import Account
from Wallet import Wallet
import unittest


class TestAccount(unittest.TestCase):
    """
    To test the account class, change the wallet_name 
    to test_wallet.json, there is all the test data located
    """

    def setUp(self):
        self.account = Account('Jose')
        self.main = self.account.get_wallet('main')
        self.emergencies = self.account.get_wallet('emergencies')
        self.charity = self.account.get_wallet('charity')
        self.savings_wallets = ['savings', 'emergencies', 'investing', 'travels', 'retirement']


    def test_account_correctly_created(self):
        """Test that the account was correctly created"""
        self.assertTrue(os.path.exists(self.account.get_wallet_name()))
        self.assertEqual(self.account.owner, 'Jose')
        self.assertEqual(len(self.account.wallets), 3)

        self.assertEqual(self.main.name, 'main')
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.main.percent, 70)
        self.assertFalse(self.main.cap)

        self.assertEqual(self.emergencies.name, 'emergencies')
        self.assertEqual(self.emergencies.balance, 500)
        self.assertEqual(self.emergencies.percent, 20)
        self.assertEqual(self.emergencies.cap, 50000)

        self.assertEqual(self.charity.name, 'charity')
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.charity.percent, 10)
        self.assertFalse(self.charity.cap)

    def test_get_wallet(self):
        """Test the get_wallet method"""
        self.assertEqual(self.main.name, 'main')
        self.assertEqual(self.emergencies.name, 'emergencies')
        self.assertEqual(self.charity.name, 'charity')

    def test_get_wallet_fails(self):
        """Nonexisting wallets return none"""
        self.assertIsNone(self.account.get_wallet('travels'))

    def test_add_wallet(self):
        """Test the add wallet feature"""
        self.account.add_wallet('home', 150, 5, 2000)
        new_wallet = self.account.get_wallet('home')
        self.assertEqual(len(self.account.wallets), 4)
        self.assertEqual(new_wallet.name, 'home')
        self.assertEqual(new_wallet.balance, 150)
        self.assertEqual(new_wallet.percent, 5)
        self.assertEqual(new_wallet.cap, 2000)

    def test_add_wallet_not_repeated(self):
        """Repeated names don't overwrite"""
        self.account.add_wallet('home', 150, 5, 2000)
        self.account.add_wallet('home')
        new_wallet = self.account.get_wallet('home')
        self.assertEqual(new_wallet.name, 'home')
        self.assertEqual(new_wallet.balance, 150)
        self.assertEqual(new_wallet.percent, 5)
        self.assertEqual(new_wallet.cap, 2000)

    def test_add_wallet_invalid_balance(self):
        """Invalid balance creates no wallet"""
        self.account.add_wallet('test', 'hi')
        self.assertIsNone(self.account.get_wallet('test'))

    def test_add_wallet_invalid_percent(self):
        """Invalid percent creates no wallet"""
        self.account.add_wallet('test2', 200, 'hi')
        self.assertIsNone(self.account.get_wallet('test2'))

    def test_add_wallet_invalid_cap(self):
        """invalid cap creates no wallet"""
        self.account.add_wallet('test3', 300, 10, 'hi')
        self.assertIsNone(self.account.get_wallet('test3'))

    def test_delete_wallet(self):
        """Test the delete wallet feature"""
        self.assertEqual(len(self.account.wallets), 3)
        self.account.delete_wallet('charity')
        self.assertEqual(len(self.account.wallets), 2)
        self.assertEqual(self.main.balance, 1700)

    def test_delete_wallet_doesnt_exist(self):
        """You cant delete wallets that doesnt exist"""
        self.assertEqual(len(self.account.wallets), 3)
        self.account.delete_wallet('test')
        self.assertEqual(len(self.account.wallets), 3)

    def test_cant_delete_main(self):
        """Main wallet is not allowed to be deleted"""
        self.account.delete_wallet('main')
        self.assertTrue(self.account.get_wallet('main'))

    def test_correct_percent(self):
        """Test the correct percent feature"""
        self.assertTrue(self.account.correct_percent())

    def test_correct_percent_above_100(self):
        """percent sum above 100 return false"""
        self.account.add_wallet('home', 100, 20)
        self.assertFalse(self.account.correct_percent())

    def test_correct_percent_below_100(self):
        """percent sum below 100 return false"""
        test_account = Account('test')
        test_account.wallets.clear()
        test_account.add_wallet('new1', 100, 20)
        test_account.add_wallet('new2', 100)
        test_account.add_wallet('new3', 100)
        test_account.add_wallet('new4', 100, 50)
        self.assertFalse(test_account.correct_percent())

    def test_correct_percent_zero(self):
        """zero percent sum return false"""
        test_account2 = Account('test2')
        test_account2.wallets.clear()
        test_account2.add_wallet('new5')
        test_account2.add_wallet('new6')
        self.assertFalse(test_account2.correct_percent())

    def test_valid_number(self):
        """Tests for the valid_number method"""
        self.assertTrue(self.account.valid_number(10))
        self.assertTrue(self.account.valid_number(0))
        self.assertFalse(self.account.valid_number('10'))
        self.assertFalse(self.account.valid_number(4.3))
        self.assertFalse(self.account.valid_number(-9))
        self.assertFalse(self.account.valid_number(True))
        self.assertFalse(self.account.valid_number(None))

    def test_transfer(self):
        """Tests for the transfer feature"""
        self.account.transfer('main', 'emergencies', 500)
        self.assertEqual(self.main.balance, 1000)
        self.assertEqual(self.emergencies.balance, 1000)

    def test_transfer_amount_surpass_wallet(self):
        """transfers where amount is greater than from balance don't carry out"""
        self.account.transfer('charity', 'emergencies', 300)
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.emergencies.balance, 500)

    def test_transfer_invalid_amount(self):
        """Invalid number formats don't trigger the transfer"""
        self.account.transfer('main', 'charity', -50)
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.main.balance, 1500)

    def test_transfer_none_amount(self):
        """Test transfer method transfering all money when amount is None"""
        self.account.transfer('charity', 'emergencies')
        self.assertEqual(self.charity.balance, 0)
        self.assertEqual(self.emergencies.balance, 700)

    def test_total(self):
        """Test Total method"""
        self.assertEqual(self.account.total(), '$2200')

    def test_total_after_deposit(self):
        """total properly works with deposit"""
        self.account.deposit(800)
        self.assertEqual(self.account.total(), '$3000')

    def test_save(self):
        """Save method correctly saves changes into JSON file"""
        # Save a new wallet to json file
        self.account.add_wallet('test', 10, 10, 10)
        self.account.save()

        # read json file and confirm new wallet values
        account = Account('Jose')
        test = account.get_wallet('test')
        self.assertEqual(len(account.wallets), 4)
        self.assertEqual(test.name, 'test')
        self.assertEqual(test.balance, 10)
        self.assertEqual(test.percent, 10)
        self.assertEqual(test.cap, 10)

        # delete new wallet and save to json file
        account.delete_wallet('test')
        main = account.get_wallet('main')
        main -= 10
        account.save()

        # read json file and confirm new wallet was deleted
        account = Account('Jose')
        self.assertEqual(len(account.wallets), 3)
        self.assertIsNone(account.get_wallet('test'))

    def test_deduct(self):
        """Deduct method correctly working"""
        self.account.deduct('main', 500)
        self.assertEqual(self.main.balance, 1000)

    def test_deduct_surpass_amount(self):
        """Cant deduct money that surpasses wallet balance"""
        self.account.deduct('charity', 1000)
        self.assertEqual(self.charity.balance, 200)

    def test_deduct_nonexisting_wallet(self):
        """operations with nonexisting wallet dont carry out"""
        self.account.deduct('no_wallet', 200)
        self.assertIsNone(self.account.get_wallet('no_wallet'))
        self.assertEqual(len(self.account), 3)

    def test_deduct_invalid_amount(self):
        """Cant deduct invalid amount number format"""
        self.account.deduct('charity', 'hi')
        self.assertEqual(self.charity.balance, 200)

    def test_deduct_default(self):
        """when no amount is given, it deducts all wallet money"""
        self.account.deduct('emergencies')
        self.assertEqual(self.emergencies.balance, 0)

    def test_deposit(self):
        """Deposit feature works correctly"""
        self.account.deposit(1000)
        self.assertEqual(self.main.balance, 2200)
        self.assertEqual(self.emergencies.balance, 700)
        self.assertEqual(self.charity.balance, 300)

    def test_deposit_invalid_amount(self):
        """no valid amount format dont carry out deposit"""
        self.account.deposit('twenty bucks')
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.emergencies.balance, 500)
        self.assertEqual(self.charity.balance, 200)

    def test_deposit_fail_correct_percent_check(self):
        """deposits with fail 100 percent dont carry out"""
        self.account.add_wallet('test', 20, 20)
        self.account.deposit(500)
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.emergencies.balance, 500)
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.account.get_wallet('test').balance, 20)

    def test_add(self):
        """Add to wallet feature works correctly"""
        self.account.add('main', 500)
        self.assertEqual(self.main.balance, 2000)

    def test_add_invalid_wallet(self):
        """cant add money to nonexisting wallets"""
        self.account.add('no wallet', 20)
        self.assertIsNone(self.account.get_wallet('no wallet'))
        self.assertEqual(len(self.account), 3)

    def test_add_invalid_amount(self):
        """dont add invalid amounts of money"""
        self.account.add('main', 'hi')
        self.assertEqual(self.main.balance, 1500)

    def test_repr(self):
        """Repr method correctly working"""
        self.assertEqual(repr(self.account), 'Account: Jose')

    def test_len(self):
        """Len function returns the amount of wallets"""
        self.assertEqual(len(self.account), 3)

    def test_reset(self):
        """Load function works properly"""
        acc = Account('test')
        acc.add_wallet('test')
        
        acc.reset()
        main = acc.get_wallet('main')
        emergencies = acc.get_wallet('emergencies')
        charity = acc.get_wallet('charity')

        self.assertEqual(len(acc.wallets), 3)
        self.assertEqual(main.name, 'main')
        self.assertEqual(main.balance, 1500)
        self.assertEqual(main.percent, 70)
        self.assertFalse(main.cap)

        self.assertEqual(emergencies.name, 'emergencies')
        self.assertEqual(emergencies.balance, 500)
        self.assertEqual(emergencies.percent, 20)
        self.assertEqual(emergencies.cap, 50000)

        self.assertEqual(charity.name, 'charity')
        self.assertEqual(charity.balance, 200)
        self.assertEqual(charity.percent, 10)
        self.assertFalse(charity.cap)

    def test_calc_percents_main_percent(self):
        """The main percent is correctly calculated"""
        percents = {'emergencies': 30, "charity": 20}
        self.account.calc_percents(percents)
        self.assertTrue(self.account.correct_percent())
        self.assertEqual(self.main.percent, 50)
        self.assertEqual(self.emergencies.percent, 30)
        self.assertEqual(self.charity.percent, 20)
        self.assertEqual(len(self.account), 3)

    def test_calc_percents_main_no_change(self):
        """Main doesn't change its percent if the sum is already 100"""
        percents = {'emergencies': 60, "charity": 40}
        self.account.calc_percents(percents)
        self.assertTrue(self.account.correct_percent())
        self.assertEqual(self.main.percent, 0)
        self.assertEqual(self.emergencies.percent, 60)
        self.assertEqual(self.charity.percent, 40)
        self.assertEqual(len(self.account), 3)

    def test_calc_percents_invalid(self):
        """Operation invalid if percents surpass 100"""
        percents = {'emergencies': 60, "charity": 60}
        self.account.calc_percents(percents)
        self.assertTrue(self.account.correct_percent())
        self.assertEqual(self.main.percent, 70)
        self.assertEqual(self.emergencies.percent, 20)
        self.assertEqual(self.charity.percent, 10)
        self.assertEqual(len(self.account), 3)

    def test_wipe(self):
        """Wipe method delets all wallets"""
        self.account.wipe()
        self.assertEqual(len(self.account), 0)

    def test_clear(self):
        """Clear method working correctly"""
        self.account.clear_all()
        self.assertEqual(len(self.account.wallets), 3)

        self.assertEqual(self.main.name, 'main')
        self.assertEqual(self.main.balance, 0)
        self.assertEqual(self.main.percent, 0)
        self.assertEqual(self.main.cap, 0)

        self.assertEqual(self.emergencies.name, 'emergencies')
        self.assertEqual(self.emergencies.balance, 0)
        self.assertEqual(self.emergencies.percent, 0)
        self.assertEqual(self.emergencies.cap, 0)

        self.assertEqual(self.charity.name, 'charity')
        self.assertEqual(self.charity.balance, 0)
        self.assertEqual(self.charity.percent, 0)
        self.assertEqual(self.charity.cap, 0)

    def test_usable(self):
        """Usable method works correctly"""
        self.assertEqual(self.account.usable(), '$1700')

    def test_non_usable(self):
        """non_usable method works correctly"""
        self.assertEqual(self.account.non_usable(), '$500')

    def test_add_wallet_fails_balance_above_cap(self):
        """You can't add wallets if the balance is higher than the cap"""
        self.account.add_wallet('test', 2000, 40, 1000)
        self.assertEqual(len(self.account), 3)
        self.assertIsNone(self.account.get_wallet('test'))

    def test_transfer_to_surpasses_cap(self):
        """
        If a transfer to a wallet surpasses the cap,
        the extra amount goes into 'main'
        """

        self.account.add_wallet('test', 0, 0, 100)
        self.account.transfer('emergencies', 'test', 200)
        test = self.account.get_wallet('test')
        self.assertEqual(self.emergencies.balance, 300)
        self.assertEqual(test.balance, 100)
        self.assertEqual(test.percent, 0)
        self.assertEqual(self.main.balance, 1600)

    def test_correct_cap_valid_wallet(self):
        """Make no changes to a valid wallet"""
        test = Wallet('test', 1000, 20, 2000)
        test2 = Wallet('test2', 2000, 30, 2000)
        
        self.account.correct_cap(test)
        self.account.correct_cap(test2)
        
        self.assertEqual(test.balance, 1000)
        self.assertEqual(test2.balance, 2000)
        self.assertEqual(test.percent, 20)
        self.assertEqual(test2.percent, 30)
    
    def test_correct_cap_invalid_wallet(self):
        """Make changes to wallets where balance surpass cap"""
        
        test = Wallet('test', 5000, 20, 2000)
        self.account.correct_cap(test)
        
        self.assertEqual(test.balance, 2000)
        self.assertEqual(test.percent, 0)
        self.assertEqual(self.main.balance, 4500)

    def test_correct_cap_main_created(self):
        """Create a main wallet and perform operations if it doesn't exist"""

        self.account.wallets.remove(self.main)
        self.assertIsNone(self.account.get_wallet('main'))

        test = Wallet('test', 5000, 20, 2000)
        self.account.correct_cap(test)
        main = self.account.get_wallet('main')
        
        self.assertEqual(test.balance, 2000)
        self.assertEqual(test.percent, 0)
        self.assertEqual(main.balance, 3000)

    def test_correct_cap_zero(self):
        """Cap zero means that there is no limit"""

        test = Wallet('test', 5000, 20, 0)
        self.account.correct_cap(test)
        
        self.assertEqual(test.balance, 5000)
        self.assertEqual(test.percent, 20)

    def test_cap_on_deposit(self):
        """Cap feature works on deposits"""

        self.emergencies.cap = 600
        self.charity.cap = 1000
        self.account.deposit(1000)

        self.assertEqual(self.main.balance, 2300)
        self.assertEqual(self.main.percent, 70)
        self.assertEqual(self.main.cap, 0)
        self.assertEqual(self.emergencies.balance, 600)
        self.assertEqual(self.emergencies.percent, 0)
        self.assertEqual(self.emergencies.cap, 600)
        self.assertEqual(self.charity.balance, 300)
        self.assertEqual(self.charity.percent, 10)
        self.assertEqual(self.charity.cap, 1000)

    def test_cap_on_add_surpass_balance(self):
        """Cap feature works on add to wallet"""

        self.charity.cap = 1000
        self.account.add('charity', 1000)

        self.assertEqual(self.charity.balance, 1000)
        self.assertEqual(self.charity.percent, 0)
        self.assertEqual(self.main.balance, 1700)

    def test_cap_on_add_valid(self):
        """Cap doesn't trigger on valid balances"""

        self.charity.cap = 1000
        self.account.add('charity', 500)

        self.assertEqual(self.charity.balance, 700)
        self.assertEqual(self.charity.percent, 10)
        self.assertEqual(self.main.balance, 1500)

    def test_set_valid_cap(self):
        """When a cap is set higher to the balance, no changes are made to main"""
        self.account.set_cap('charity', 300)
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.charity.balance, 200)
        self.assertEqual(self.charity.percent, 10)
    
    def test_set_invalid_cap(self):
        """When a cap is set higher to the balance, no changes are made to main"""
        self.account.set_cap('emergencies', 300)
        self.assertEqual(self.main.balance, 1700)
        self.assertEqual(self.emergencies.balance, 300)
        self.assertEqual(self.emergencies.percent, 0)

    def test_set_invalid_cap_value(self):
        """Don't do anything if the cap value is invalid"""
        self.account.set_cap('emergencies', 'hi')
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.emergencies.balance, 500)
        self.assertEqual(self.emergencies.percent, 20)
        self.assertEqual(self.emergencies.cap, 50000)

    def test_cant_set_cap_main(self):
        """Setting the cap attribute on main is not allowed"""
        self.account.set_cap('main', 500)
        self.assertEqual(self.main.balance, 1500)
        self.assertEqual(self.main.percent, 70)
        self.assertEqual(self.main.cap, 0)

    def test_rename_valid_wallet(self):
        """Rename works correctly on an existing wallet"""
        self.account.rename('charity', 'givings')
        self.assertEqual(len(self.account), 3)
        self.assertTrue(self.account.get_wallet('givings'))
        self.assertEqual(self.charity.name, 'givings')

    def test_rename_invalid_main(self):
        """Rename doesn't work on main"""
        self.account.rename('main', 'principal')
        self.assertEqual(self.main.name, 'main')

    def test_rename_non_existing_wallet(self):
        """Can't rename a nonexistant wallet"""
        self.account.rename('test', 'unit')
        self.assertEqual(len(self.account), 3)
        self.assertEqual(self.main.name, 'main')
        self.assertEqual(self.charity.name, 'charity')
        self.assertEqual(self.emergencies.name, 'emergencies')

    def test_clear_wallet(self):
        """Test clear wallet works correctly"""
        self.account.clear('emergencies')
        self.assertEqual(self.emergencies.balance, 0)
        self.assertEqual(self.emergencies.percent, 0)
        self.assertEqual(self.emergencies.cap, 0)


if __name__ == '__main__':
    unittest.main()