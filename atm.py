class Card:
    def __init__(self, card_number: str, pin: str):
        self.card_number = card_number
        self.pin = pin

    def validate_pin(self, input_pin: str) -> bool:
        return self.pin == input_pin

class ATMController:
    def __init__(self):
        self.inserted_card = None

    def insert_card(self, card: Card) -> bool:
        if card:
            self.inserted_card = card
            return True
        return False