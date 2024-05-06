import os
import json
import logging

from models import Wallet

#############
# Projects consts
#############

MAIN_MENUE_TEXT = (
    "1. Add transaction\n"
    "2. Delete transaction\n"
    "3. Get transactions list\n"
    "4. Edit transaction \n"
    "5. Exit \n"
    "Select command: "
)

DELETE_MENUE_TEXT = "Select transaction for delete: "

EXIT_MENUE = "You want to close the script?"

wallet = Wallet()

#############
# Formatter's func
#############


def cls() -> None:
    """Clean terminal func."""
    os.system("cls" if os.name == "nt" else "clear")


def input_transaction_data() -> list:
    """Request category, value, description of transaction."""
    while True: #category input, only R/D?
        category = str(input("Select category(Расход(R)/Доход(D)): ")).lower()
        if category not in ["r", "d"]:
            cls()
            logging.warning('Wrong type category: %s should be "r" or "d".', category)
            print("Wrong type, input (R/D)...")
            continue
        break
    while True: #value input, only INT?
        value = input("Input Value: ")
        if not value.isdigit():
            cls()
            print("Wrong type, input integer...")
            logging.warning(
                "Wrong type of transaction value: %s should be int", type(value)
            )
            continue
        value = int(value)
        break
    description = input("Input description: ")
    return [category, value, description]

def print_transactions_list(transactions: list) -> None:
    """Formated transactions list print."""
    counter = 1
    print("#" * 50)
    for t in transactions:
        print(f'{" "*25}№{counter}')
        counter += 1
        print(json.dumps(t, indent=4))
        print("#" * 50)

#############
# Entry point
#############

def main() -> None:
    """Main func."""
    command = 0
    while True:
        cls()
        print(f"Balance: {wallet.balance}.")
        match command:
            case 0: #for clear terminal
                command = int(input(MAIN_MENUE_TEXT))
            case 1: #for add transaction
                category, value, description = input_transaction_data()
                wallet.add_transaction(category, value, description)
                cls()
                print(f"Balance: {wallet.balance}.")
                command = int(input(MAIN_MENUE_TEXT))
            case 2: # for delete transaction
                transactions = wallet.read_transactions()
                transactions = transactions["transactions"]
                print_transactions_list(transactions)
                command = int(input(DELETE_MENUE_TEXT))
                if not(wallet.delete_transaction(command - 1)):
                    cls()
                    print('#Index error...')
                    command = int(input(MAIN_MENUE_TEXT))
                    continue
                cls()
                print('#Transaction was deleted...')
                command = int(input(MAIN_MENUE_TEXT))
            case 3:# for print transactions list
                transactions = wallet.read_transactions()
                transactions = transactions["transactions"]
                print_transactions_list(transactions)
                print(f"Balance: {wallet.balance}.")
                command = int(input(MAIN_MENUE_TEXT))
            case 4:#for edit transaction
                transactions = wallet.read_transactions()
                transactions = transactions["transactions"]
                print_transactions_list(transactions)
                position = input('Select transaction for edit: ')
                while not (position.isdigit()):
                    print('#Input transaction id: int...')
                    position = input('Select transaction for edit: ')
                position = int(position)
                resp = wallet.edit_transaction(position-1,input_transaction_data())
                cls()
                if not resp:
                    print('#Index out of range...')
                else:
                    print('#Transaction was deleted...')
                command = int(input(MAIN_MENUE_TEXT))
            case 5: #for exit
                break

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="main.log",
        filemode="a",
        format=("%(asctime)s - %(levelname)s - %(message)s"),
    )
    main()
