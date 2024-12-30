class Account:
    def __init__(self, account_number: str, balance: int):
        self.account_number = account_number
        self.balance = balance

    def get_balance(self) -> int:
        return self.balance

    def withdraw(self, amount: int) -> bool:
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

class Card:
    def __init__(self, card_number: str, pin: str, accounts: list):  # accounts 매개변수 추가
        self.card_number = card_number
        self.pin = pin
        self.accounts = accounts

    def get_accounts(self) -> list:  # 새로운 메서드
        return self.accounts

class ATMController:
    def __init__(self):
        self.inserted_card = None
        self.is_authenticated = False  # 추가

    def insert_card(self, card: Card) -> bool:
        if card:
            self.inserted_card = card
            self.is_authenticated = False  # 카드 삽입시 인증 상태 초기화
            return True
        return False

    def validate_pin(self, pin: str) -> bool:  # 새로운 메서드
        if self.inserted_card and self.inserted_card.validate_pin(pin):
            self.is_authenticated = True
            return True
        return False