import unittest

class TestATMController(unittest.TestCase):
    def setUp(self):
        self.atm = ATMController()
        self.card = Card("123456", "1234")

    def test_insert_card(self):
        self.assertTrue(self.atm.insert_card(self.card))
        self.assertFalse(self.atm.insert_card(None))