import uuid
import json
import logging

from datetime import date


class Transaction:
    """Transaction Model"""

    def __init__(self, category: str, value: int, description: str, **kwargs):
        self.date = kwargs.get("date", str(date.today()))
        self.category = category
        self.value = value
        self.description = description
        self.id = kwargs.get("id", str(uuid.uuid1()))

    def get_transaction_data(self) -> dict:
        return {
            "date": self.date,
            "category": self.category,
            "value": self.value,
            "description": self.description,
            "id": self.id,
        }

    @classmethod
    def json_build(cls, json_data):
        return cls(**json_data)


class Wallet:
    """'Wallet model"""

    def __init__(self):
        self.balance: int = 0
        self.transactions_count: int
        self.transactions = self.init_transactions()

    def init_transactions(self) -> list:
        transactions_in_f = self.read_transactions()["transactions"]
        transactions = []
        for t in transactions_in_f:
            transaction = Transaction.json_build(t)
            transactions.append(transaction)
        return transactions

    #############
    # Wallet handlers
    #############

    def change_value(self, action_type: str, value: int) -> None:
        """change wallet balance"""
        if action_type == "r":
            self.balance -= value
        else:
            self.balance += value
        logging.info("Balance was changed, current balance: %s.", self.balance)

    #############
    # Transactions handlers
    #############

    def get_transactions(self) -> list[Transaction]:
        """Get wallets transactions list method."""
        return self.transactions

    def add_transaction(self, category: str, value: int, description: str) -> bool:
        """Add transactions method."""
        transaction = Transaction(category, value, description)
        self.transactions.append(transaction)
        self.change_value(category, value)
        logging.info("Add transaction: %s : %s", category, value)
        self.write_transaction(transaction)
        return True

    def delete_transaction(self, position: int) -> bool:
        """'Delete transaction method."""
        print(len(self.transactions))
        if position>=len(self.transactions) or position <= 0:
            logging.warning('Position for delete out of range: %s, max: %s}', position, len(self.transactions))
            return False
        pk = self.transactions[position].id
        self.delete_transaction_from_json(pk)
        self.transactions.pop(position)
        return True

    #############
    # Json file handlers
    #############

    def write_transaction(self, transaction: Transaction):
        """Write transaction in json file."""
        transaction = transaction.get_transaction_data()
        data = self.read_transactions()
        data["transactions"].append(transaction)
        with open("transactions.json", "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Write transaction in json id: %s", transaction.get("id"))

    def delete_transaction_from_json(self, pk):
        data = self.read_transactions()["transactions"]
        filtred_data = [t for t in data if t.get("id") != pk]
        data = {}
        data["transactions"] = filtred_data
        with open("transactions.json", "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Write transaction in json id: %s", pk)

    def read_transactions(self):
        try:
            with open("transactions.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"transactions": []}
        return data
