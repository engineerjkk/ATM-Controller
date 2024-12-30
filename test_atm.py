class TestATMController(unittest.TestCase):
    def setUp(self):
        self.atm = ATMController()
        self.card = Card("123456", "1234")

    def test_insert_card(self):
        self.assertTrue(self.atm.insert_card(self.card))
        self.assertFalse(self.atm.insert_card(None))

    def test_pin_validation(self):  # 새로운 테스트
        self.atm.insert_card(self.card)
        self.assertTrue(self.atm.validate_pin("1234"))
        self.assertFalse(self.atm.validate_pin("wrong"))