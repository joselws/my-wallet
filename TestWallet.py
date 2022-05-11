from Wallet import Wallet
import unittest

class TestWallet(unittest.TestCase):
    """Testing the class Wallet"""

    def test_wallet_no_name(self):
        """Wallet without the required attribute name returns NameError"""
        with self.assertRaises(TypeError):
                error = Wallet()

    def test_wallet_correctly_created_default_values(self):
        """Correct Wallet creation"""
        base = Wallet('Base')
        self.assertIsNone(base.percent)
        self.assertIsNone(base.cap)
        self.assertEqual(base.name, "Base")
        self.assertEqual(base.balance, 0)
        self.assertEqual(repr(base), 'Base: $0')

    def test_wallet_all_values(self):
        """Provide all data to this wallet"""
        emergencies = Wallet('Emergencies', 100, 15, 80000)
        self.assertEqual(emergencies.percent, 15)
        self.assertEqual(emergencies.cap, 80000)
        self.assertEqual(emergencies.name, "Emergencies")
        self.assertEqual(emergencies.balance, 100)
        self.assertEqual(repr(emergencies), 'Emergencies: $100')

    def test_add(self):
        """Test the __add__ method of this wallet"""
        test_wallet = Wallet('Test', 50)
        self.assertEqual(test_wallet.balance, 50)
        self.assertIsNone(test_wallet.percent)
        self.assertIsNone(test_wallet.cap)
        
        test_wallet += 50
        self.assertEqual(test_wallet.balance, 100)

    def test_sub(self):
        """Test the __sub__ method of this wallet"""
        test_wallet = Wallet('Test', balance=50)
        self.assertEqual(test_wallet.balance, 50)
        self.assertIsNone(test_wallet.percent)
        self.assertIsNone(test_wallet.cap)
        
        test_wallet -= 50
        self.assertEqual(test_wallet.balance, 0)

if __name__ == "__main__":
    unittest.main()