import logging

from models import Wallet, Transaction


MAIN_MENUE_TEXT = (
    '1. Add transaction\n'
    '2. Delete transaction\n'
    '3. Get transactions list\n'
    '4. Exit'
    'Select command: '
)

DELETE_MENUE_TEXT = ('Select transaction for delete: ')

EXIT_MENUE = ('You want to close the script?')

def command_handler():
    message = MAIN_MENUE_TEXT
    command = input('Select command: ')


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        filemode='a',
        format=('%(asctime)s - %(levelname)s - %(message)s'),
    )
    wallet = Wallet()
    wallet.add_transaction()
    wallet.add_transaction()
    print([x.get_transaction_data() for x in wallet.get_transactions()])
    print(wallet.balance)


if __name__ == '__main__':
    main()
