from datetime import datetime, timedelta

class Card:
    def __init__(self, card_number: str, pin: str, accounts: list):
        self.card_number = card_number
        self.pin = pin
        self.accounts = accounts

    def validate_pin(self, input_pin: str) -> bool:
        return self.pin == input_pin

    def get_accounts(self) -> list:
        return self.accounts

class Transaction:
    def __init__(self, transaction_type: str, amount: int, balance: int):
        self.timestamp = datetime.now()
        self.type = transaction_type
        self.amount = amount
        self.balance = balance

class Account:
   MAX_WITHDRAWAL = 1000
   MAX_DEPOSIT = 5000

   def __init__(self, account_number: str, balance: int):
       self.account_number = account_number
       self.balance = balance
       self.transactions = []

   def get_balance(self) -> int:
       return self.balance

   def add_transaction(self, type: str, amount: int):
       transaction = Transaction(type, amount, self.balance)
       self.transactions.append(transaction)

   def withdraw(self, amount: int) -> bool:
       if amount > self.MAX_WITHDRAWAL:
           print(f"Withdrawal amount exceeds the maximum limit (${self.MAX_WITHDRAWAL})")
           return False
       if amount > self.balance:
           print("Insufficient balance")
           return False
       self.balance -= amount
       self.add_transaction("withdrawal", amount)
       return True

   def deposit(self, amount: int) -> bool:
       if amount > self.MAX_DEPOSIT:
           print(f"Deposit amount exceeds the maximum limit (${self.MAX_DEPOSIT})")
           return False
       self.balance += amount
       self.add_transaction("deposit", amount)
       return True

   def get_transaction_history(self):
       return self.transactions


class ATMController:
    SESSION_TIMEOUT = 30

    def __init__(self):
        self.inserted_card = None
        self.is_authenticated = False
        self.selected_account = None
        self.last_activity = None
        self.reset_session()

    def insert_card(self, card: Card) -> bool:
        if card:
            print(f"Card inserted. Card number: {card.card_number}")
            self.inserted_card = card
            self.is_authenticated = False
            return True
        print("Card insertion failed")
        return False

    def validate_pin(self, pin: str) -> bool:
        if not pin.isdigit() or len(pin) != 4:
            print("PIN must be a 4-digit number")
            return False
            
        if self.inserted_card and self.inserted_card.validate_pin(pin):
            print("PIN validation successful")
            self.is_authenticated = True
            return True
        print("Invalid PIN")
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
        if self.check_timeout():
            raise Exception("Session expired")
            
        if self.selected_account:
            self.update_activity()
            return self.selected_account.get_balance()
        raise Exception("No account selected")

    def withdraw(self, amount: int) -> bool:
        if self.check_timeout():
            return False
            
        if not isinstance(amount, int) or amount <= 0:
            print("Please enter a valid amount")
            return False
                
        if self.selected_account:
            result = self.selected_account.withdraw(amount)
            print(f"Withdrawal {'successful' if result else 'failed'}: ${amount}")
            self.update_activity()
            return result
        print("No account selected")
        return False

    def deposit(self, amount: int) -> bool:
        if not isinstance(amount, int) or amount <= 0:
            print("Please enter a valid amount")
            return False
            
        if self.check_timeout():
            return False
            
        if self.selected_account:
            result = self.selected_account.deposit(amount)
            print(f"Deposit {'successful' if result else 'failed'}: ${amount}")
            self.update_activity()
            return result
        print("No account selected")
        return False

    def eject_card(self):
        self.inserted_card = None
        self.selected_account = None
        self.is_authenticated = False

    def reset_session(self):
        self.inserted_card = None
        self.is_authenticated = False
        self.selected_account = None
        self.last_activity = None

    def check_timeout(self) -> bool:
        if not self.last_activity:
            return False
        if datetime.now() - self.last_activity > timedelta(seconds=self.SESSION_TIMEOUT):
            print("Session expired. Please insert your card again.")
            self.reset_session()
            raise Exception("Session expired")
        return False

    def update_activity(self):
        self.last_activity = datetime.now()


if __name__ == "__main__":
   # Create test data
   account = Account("12345", 1000)
   card = Card("9876", "1234", [account])
   atm = ATMController()
   
   # Example usage
   atm.insert_card(card)
   atm.validate_pin(input("Enter PIN: "))
   atm.select_account(account)
   print(f"Current balance: ${atm.check_balance()}")
   
   # Test withdrawal
   amount = int(input("Enter amount to withdraw: "))
   atm.withdraw(amount)
   print(f"Balance after withdrawal: ${atm.check_balance()}")