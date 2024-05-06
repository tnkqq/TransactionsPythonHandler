import uuid
import json
import logging
import datetime
from datetime import date


class Transaction:
    """Transaction Model"""

    def __init__(self, category: str, value: int, description: str, **kwargs):
        self.date = kwargs.get("date", str(datetime.datetime.now()))
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

    def edit_transaction(self, date: str, id: int, *args):
        params = args[0]
        self.id = id
        self.date = date
        self.category, self.value, self.description = params

    @classmethod
    def json_build(cls, json_data):
        return cls(**json_data)


class Wallet:
    """'Wallet model"""

    def __init__(self):
        self.balance: int = 0
        self.transactions_count: int
        self.transactions: list = self.init_transactions()

    def init_transactions(self) -> list:
        transactions_in_f = self.read_transactions()["transactions"]
        transactions = []
        for t in transactions_in_f:
            transaction = Transaction.json_build(t)
            transactions.append(transaction)
            if t.get('category') == 'r':
                self.balance-=t.get('value')
            else:
                self.balance+=t.get('value')
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
        self.__write_transaction(transaction)
        return True

    def delete_transaction(self, position: int) -> bool:
        """'Delete transaction method."""
        if position>=len(self.transactions) or position < 0:
            logging.warning('Position for delete out of range: %s, max: %s}', position, len(self.transactions))
            return False
        transaction = self.transactions[position]
        if transaction.category == 'r':
            self.balance += transaction.value
        else:
            self.balance -= transaction.value
        pk = self.transactions[position].id
        self.__delete_transaction_from_json(pk)
        self.transactions.pop(position)
        return True

    def edit_transaction(self, position: int, *args) -> bool:
        if position>=len(self.transactions) or position < 0:
            logging.warning('Position for edit out of range: %s, max: %s}', position, len(self.transactions))
            return False
        transaction = self.transactions[position]
        self.__delete_transaction_from_json(transaction.id)
        transaction.edit_transaction(transaction.date, transaction.id,*args)
        self.change_value(transaction.category, transaction.value)
        self.__write_transaction(transaction)
        return True

    #############
    # Json file handlers
    #############

    def __write_transaction(self, transaction: Transaction) -> bool:
        """Write transaction in json file."""
        transaction = transaction.get_transaction_data()
        data = self.read_transactions()
        data["transactions"].append(transaction)
        with open("transactions.json", "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Write transaction in json id: %s", transaction.get("id"))
        return True 

    def __delete_transaction_from_json(self, pk: str) -> bool:
        '''Delete transaction from json file method.'''
        data = self.read_transactions()["transactions"]
        filtred_data = [t for t in data if t.get("id") != pk]
        data = {}
        data["transactions"] = filtred_data
        with open("transactions.json", "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Write transaction in json id: %s", pk)
        return True 

    def read_transactions(self) -> dict:
        '''Read transactions from json file method.'''
        try:
            with open("transactions.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"transactions": []}
        return data
