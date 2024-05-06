import pytest

from models import Wallet, Transaction
@pytest.fixture
def wallet():
    wallet = Wallet()
    return wallet

@pytest.fixture
def transaction(wallet):
    CATEGORY = 'D'
    VALUE = 2000
    DESCRIPTION = 'test_description'
    wallet.add_transaction(CATEGORY, VALUE, DESCRIPTION)
    transaction = wallet.transactions[-1]
    return transaction
