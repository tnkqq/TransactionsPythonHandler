from models import Wallet, Transaction

VALUE = 2000
DESCRIPTION = 'test_description'


def test_add_transaction(wallet):
    current_transactions_count = len(wallet.transactions)
    wallet.add_transaction('b',VALUE, DESCRIPTION)
    new_count_transactions = len(wallet.transactions)
    assert new_count_transactions == current_transactions_count+1

def test_delete_transaction(wallet):
    current_transactions_count = len(wallet.transactions)
    wallet.delete_transaction(1)
    new_count_transactions = len(wallet.transactions)
    assert new_count_transactions == current_transactions_count-1

def test_edit_transaction(wallet, transaction):
    NEW_CATEGORY = 'd'
    NEW_VALUE = VALUE + 1000
    NEW_DESCRIPTION = 'NEW_DESCRIPTION'
    current_len = len(wallet.transactions)
    start_data = transaction.get_transaction_data() 
    wallet.edit_transaction(current_len-1,[NEW_CATEGORY,NEW_VALUE, NEW_DESCRIPTION])
    new_data = wallet.transactions[current_len-1].get_transaction_data()
    assert new_data['category'] == NEW_CATEGORY
    assert new_data['value'] == NEW_VALUE
    assert new_data['description'] == NEW_DESCRIPTION
    assert new_data['id'] == start_data['id']
