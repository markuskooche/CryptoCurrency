from crypto_currency.blockchain import BlockChain


def get_accounts():
    blocks = BlockChain.get_blockchain()
    name_list = set()

    for block in blocks:
        transaction = block['transaction']

        if len(transaction) == 3:
            name_list.add(transaction.get('recipient'))
    
    return name_list


def get_transactions(name):
    blocks = BlockChain.get_blockchain()
    transactions = 0

    for block in blocks:
        data = block['transaction']

        if len(data) == 3:
            if data.get('recipient') == name:
                transactions += 1

            if data.get('sender') == name:
                transactions += 1
    
    return transactions


def get_coins(name):
    blocks = BlockChain.get_blockchain()
    coins = 0

    for block in blocks:
        data = block['transaction']

        if len(data) == 3:
            if data.get('recipient') == name:
                coins += data.get('quantity') 

            if data.get('sender') == name:
                coins -= data.get('quantity')

    return coins
