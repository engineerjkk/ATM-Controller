class Card:
   def __init__(self, card_number: str, pin: str, accounts: list):
       self.card_number = card_number
       self.pin = pin
       self.accounts = accounts

   def validate_pin(self, input_pin: str) -> bool:
       return self.pin == input_pin

   def get_accounts(self) -> list:
       return self.accounts


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

   def deposit(self, amount: int):
       self.balance += amount


class ATMController:
   def __init__(self):
       self.inserted_card = None
       self.is_authenticated = False
       self.selected_account = None

   def insert_card(self, card: Card) -> bool:
       if card:
           print(f"카드가 삽입되었습니다. 카드번호: {card.card_number}")
           self.inserted_card = card
           self.is_authenticated = False
           return True
       print("카드 삽입 실패")
       return False

   def validate_pin(self, pin: str) -> bool:
       if not pin.isdigit() or len(pin) != 4:
           print("PIN은 4자리 숫자여야 합니다.")
           return False
           
       if self.inserted_card and self.inserted_card.validate_pin(pin):
           print("PIN 인증 성공")
           self.is_authenticated = True
           return True
       print("잘못된 PIN입니다.")
       return False

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

   def withdraw(self, amount: int) -> bool:
       if not isinstance(amount, int) or amount <= 0:
           print("올바른 금액을 입력하세요")
           return False
           
       if self.selected_account:
           result = self.selected_account.withdraw(amount)
           print(f"출금 {'성공' if result else '실패'}: {amount}달러")
           return result
       print("계좌가 선택되지 않았습니다")
       return False

   def deposit(self, amount: int):
       if self.selected_account:
           self.selected_account.deposit(amount)
           return
       raise Exception("계좌가 선택되지 않았습니다")

   def eject_card(self):
       self.inserted_card = None
       self.selected_account = None
       self.is_authenticated = False


if __name__ == "__main__":
   # 테스트용 데이터 생성
   account = Account("12345", 1000)
   card = Card("9876", "1234", [account])
   atm = ATMController()
   
   # 실행 예시
   atm.insert_card(card)
   atm.validate_pin(input("PIN을 입력하세요: "))
   atm.select_account(account)
   print(f"현재 잔액: {atm.check_balance()}")
   
   # 출금 테스트
   amount = int(input("출금할 금액을 입력하세요: "))
   atm.withdraw(amount)
   print(f"출금 후 잔액: {atm.check_balance()}")