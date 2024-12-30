class Card:
    def __init__(self, card_number: str, pin: str):
        self.card_number = card_number
        self.pin = pin

    def validate_pin(self, input_pin: str) -> bool:
        return self.pin == input_pin

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