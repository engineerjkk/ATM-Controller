import unittest
from atm import Account, Card, ATMController
import time
from datetime import datetime, timedelta

class TestATMController(unittest.TestCase):
    def setUp(self):
        self.atm = ATMController()
        account1 = Account("1", 1000)
        self.card = Card("123456", "1234", [account1])

    def test_insert_card(self):
        self.assertTrue(self.atm.insert_card(self.card))
        self.assertFalse(self.atm.insert_card(None))

    def test_pin_validation(self):
        self.atm.insert_card(self.card)
        self.assertTrue(self.atm.validate_pin("1234"))
        self.assertFalse(self.atm.validate_pin("wrong"))

    def test_account_operations(self):
        account = Account("1", 1000)
        self.assertEqual(account.get_balance(), 1000)
        self.assertTrue(account.withdraw(500))
        self.assertEqual(account.get_balance(), 500)
        self.assertFalse(account.withdraw(1000))

    def test_account_selection(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        self.assertTrue(self.atm.select_account(self.card.get_accounts()[0]))
        self.assertEqual(self.atm.check_balance(), 1000)

    def test_withdraw_and_deposit(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        self.atm.select_account(self.card.get_accounts()[0])
        
        self.assertTrue(self.atm.withdraw(500))
        self.assertEqual(self.atm.check_balance(), 500)
        
        self.atm.deposit(300)
        self.assertEqual(self.atm.check_balance(), 800)

    def test_card_ejection(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        self.atm.select_account(self.card.get_accounts()[0])
        
        self.atm.eject_card()
        with self.assertRaises(Exception):
            self.atm.check_balance()

    def test_transaction_limits(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        self.atm.select_account(self.card.get_accounts()[0])
        
        # Test withdrawal limit
        self.assertFalse(self.atm.withdraw(1500))  # Exceeds limit
        
        # Test deposit limit
        self.atm.deposit(3000)  # Normal deposit
        self.assertFalse(self.atm.deposit(6000))  # Exceeds limit

    def test_transaction_history(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        account = self.card.get_accounts()[0]
        self.atm.select_account(account)
        
        # Execute transactions
        self.atm.withdraw(300)
        self.atm.deposit(500)
        
        # Check transaction history
        history = account.get_transaction_history()
        self.assertEqual(len(history), 2)
        
        # Verify latest transaction
        latest = history[-1]
        self.assertEqual(latest.type, "deposit")
        self.assertEqual(latest.amount, 500)
        self.assertEqual(latest.balance, 1200)

    def test_session_timeout(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        self.atm.select_account(self.card.get_accounts()[0])
        
        # Simulate session timeout
        self.atm.last_activity = datetime.now() - timedelta(seconds=31)
        
        with self.assertRaises(Exception):
            self.atm.check_balance()
        
        self.assertIsNone(self.atm.inserted_card)
        self.assertFalse(self.atm.is_authenticated)

    def test_invalid_pin_format(self):
        self.atm.insert_card(self.card)
        self.assertFalse(self.atm.validate_pin("12"))  # Too short!
        self.assertFalse(self.atm.validate_pin("12345"))  # Too long!
        self.assertFalse(self.atm.validate_pin("abcd"))  # Contains letters!

if __name__ == '__main__':
    unittest.main()