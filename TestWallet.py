from Wallet import Wallet
import unittest

class TestWallet(unittest.TestCase):
    """Testing the class Wallet"""

    def test_wallet_correctly_created_default_values(self):
        """Correct Wallet creation"""
        base = Wallet('Base')
        self.assertIsNone(base.percent)
        self.assertIsNone(base.cap)
        self.assertEqual(base.name, "Base")
        self.assertEqual(base.balance, 0)
        self.assertEqual(repr(base), 'Base: $0 (None%)')

    def test_wallet_all_values(self):
        """Provide all data to this wallet"""
        emergencies = Wallet('Emergencies', 15, 100, 80000)
        self.assertEqual(emergencies.percent, 15)
        self.assertEqual(emergencies.cap, 80000)
        self.assertEqual(emergencies.name, "Emergencies")
        self.assertEqual(emergencies.balance, 100)
        self.assertEqual(repr(emergencies), 'Emergencies: $100 (15%)')


if __name__ == "__main__":
    unittest.main()