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
        
        # 출금한도 테스트
        self.assertFalse(self.atm.withdraw(1500))  # 한도 초과
        
        # 입금한도 테스트
        self.atm.deposit(3000)  # 정상 입금
        self.assertFalse(self.atm.deposit(6000))  # 한도 초과

    def test_transaction_history(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        account = self.card.get_accounts()[0]
        self.atm.select_account(account)
        
        # 거래 실행
        self.atm.withdraw(300)
        self.atm.deposit(500)
        
        # 거래 내역 확인
        history = account.get_transaction_history()
        self.assertEqual(len(history), 2)
        
        # 최근 거래 확인
        latest = history[-1]
        self.assertEqual(latest.type, "입금")
        self.assertEqual(latest.amount, 500)
        self.assertEqual(latest.balance, 1200)

    def test_session_timeout(self):
        self.atm.insert_card(self.card)
        self.atm.validate_pin("1234")
        self.atm.select_account(self.card.get_accounts()[0])
        
        # 세션 타임아웃 시뮬레이션
        self.atm.last_activity = datetime.now() - timedelta(seconds=31)
        
        with self.assertRaises(Exception):
            self.atm.check_balance()
        
        self.assertIsNone(self.atm.inserted_card)
        self.assertFalse(self.atm.is_authenticated)

    def test_invalid_pin_format(self):
        self.atm.insert_card(self.card)
        self.assertFalse(self.atm.validate_pin("12"))  # 짧은 PIN의 경우
        self.assertFalse(self.atm.validate_pin("12345"))  # 긴 PIN의 경우
        self.assertFalse(self.atm.validate_pin("abcd"))  # 문자 포함의 경우 

if __name__ == '__main__':
    unittest.main()