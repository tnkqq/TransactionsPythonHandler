import uuid
import logging
from datetime import date


class Transaction:
    '''Transaction Model'''
    def __init__(self, category: str, value: int, description: str):
        self.date = date.today()
        self.category = category
        self.value = value
        self.description = description
        self.id = uuid.uuid1()

    def get_transaction_data(self) -> dict:
        return {
            "date": self.date,
            "category": self.category,
            "value": self.value,
            "description": self.description,
            "id": self.id,
        }


class Wallet:
    ''''Wallet model'''
    def __init__(self):
        self.balance: int = 0
        self.transactions_count: int
        self.transactions: list = []

    #############
    #Wallet handlers
    #############
    
    def change_value(self, action_type: str, value: int) -> None:
        '''change wallet balance'''
        if action_type == "r":
            self.balance -= value
        else:
            self.balance += value
        logging.info(f"Balance was changed, current balance: {self.balance}")

    #############
    #Transactions handlers
    #############

    def get_transactions(self) -> list[Transaction]:
        """Get wallets transactions list method."""
        return self.transactions

    def delete_transaction(self, position: int) -> bool:
        """'Delete transaction method."""
        id = self.transactions[position-1].id
        self.transactions.pop(position)
        self.delete_transaction_from_json(id)

    def add_transaction(self) -> bool:
        """Add transactions method."""
        description = "..."
        while True:
            category = str(input("Select category(Расход(R)/Доход(D)): ")).lower()
            if category not in ["r", "d"]:
                logging.warning(
                    f'Wrong type category: {category} should be "r" or "d".'
                )
                print("Wrong type, input (R/D)")
                continue
            break
        while True:
            value = int(input("Input Value: "))
            if not isinstance(value, int):
                print("Wrong type, input integer...")
                logging.warning(
                    f"Wrong type of transaction value: {type(value)} should be int"
                )
                continue
            break
        description = input("Input description: ")
        transaction = Transaction(category, value, description)
        self.transactions.append(transaction)
        self.change_value(category, value)
        logging.info(f"Add transaction: {category} : {value}")
        return True

    #############
    #Json file handlers
    #############

    def write_transaction(self, transaction: Transaction):
        """Write transaction in json file."""
        ...

    def read_transactions(self): ...