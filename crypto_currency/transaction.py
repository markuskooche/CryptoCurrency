from crypto_currency.account_details import get_coins


def add_transaction(blockchain, para_sender, para_recipient, para_quantity):
    coins = get_coins(para_sender)
    if (coins - para_quantity) < 0:
        print('Sie haben nicht genügend MarkusCoins um diese Transaktion durchzuführen!')
        exit()
    else:
        print('Die Transaktion wird durchgeführt...')
    
    last_block = blockchain.last_block
    last_proof_no = last_block.proof_no
    proof_no = blockchain.proof_of_work(last_proof_no)

    blockchain.new_data(
        sender=para_sender,
        recipient=para_recipient,
        quantity=para_quantity
    )

    last_hash = last_block.calculate_hash
    block = blockchain.construct_block(proof_no, last_hash)
    print('Sie haben erfolgreich', para_recipient, para_quantity, 'MarkusCoin transferiert!')
