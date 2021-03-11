#!/usr/bin/env python3
from crypto_currency.account_details import get_coins
from crypto_currency.transaction import add_transaction
from crypto_currency.blockchain import BlockChain


if __name__ == "__main__":
    blockchain = BlockChain()

    blockchain.block_mining('Thomas Mailer')
    print(f'Steffan Ross: {get_coins("Steffan Ross")}')
    print(f'Thomas Mailer: {get_coins("Thomas Mailer")}')

    add_transaction(blockchain, 'Thomas Mailer', 'Steffan Ross', 1)

    print(f'Steffan Ross: {get_coins("Steffan Ross")}')
    print(f'Thomas Mailer: {get_coins("Thomas Mailer")}')
