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
        self.is_authenticated = False
        self.selected_account = None  # 추가

    def get_accounts(self) -> list:
        if self.is_authenticated and self.inserted_card:
            return self.inserted_card.get_accounts()
        return []

    def select_account(self, account: Account) -> bool:
        if self.is_authenticated and account in self.get_accounts():
            self.selected_account = account
            return True
        return False

    def check_balance(self) -> int:
        if self.selected_account:
            return self.selected_account.get_balance()
        raise Exception("계좌가 선택되지 않았습니다")