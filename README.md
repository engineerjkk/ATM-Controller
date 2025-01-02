# ATM Controller Implementation

A simple ATM controller implementation focusing on basic ATM operations without UI integration. The project demonstrates clean code architecture and testability while simulating core ATM functionalities.

## Features

- Card insertion and PIN validation
- Account selection and balance checking 
- Deposit and withdrawal operations with limits
- Transaction history tracking
- Session timeout management
- Comprehensive test coverage

## Requirements

- Python 3.6 or higher
- unittest (included in Python standard library)

## Project Structure

```
.
├── README.md
├── atm.py           # Main implementation
└── test_atm.py      # Test suite
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/engineerjkk/ATM-Controller.git
cd /ATM-Controller
```

2. No additional dependencies required as the project uses Python standard library.

## Running Tests

Execute the test suite:
```bash
python -m unittest test_atm.py -v
```

## Usage Example

```python
from atm import Account, Card, ATMController

# Create test account and card
account = Account("12345", 1000)  # Account number and initial balance
card = Card("9876", "1234", [account])  # Card number, PIN, and linked accounts
atm = ATMController()

# Basic ATM operations
atm.insert_card(card)
atm.validate_pin("1234")
atm.select_account(account)

# Check balance
balance = atm.check_balance()
print(f"Current balance: ${balance}")

# Perform withdrawal
atm.withdraw(500)

# Perform deposit
atm.deposit(1000)

# End session
atm.eject_card()
```

## Implementation Notes

- Currency is handled in whole dollar amounts (no cents)
- Maximum withdrawal limit: $1,000 per transaction
- Maximum deposit limit: $5,000 per transaction
- Session timeout: 30 seconds
- PIN must be exactly 4 digits

## Future Integration Points

The code is designed for future integration with:
- Bank systems (via PIN validation and transaction processing)
- ATM hardware (card reader, cash bin)
- User interface (graphical or console-based)
