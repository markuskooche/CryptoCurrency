from crypto_currency.block import Block
import hashlib, json, time


class BlockChain():
    def __init__(self):
        self.chain = []
        self.index = 0
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()

    # CREATE THE BLOCKCHAIN
    def construct_genesis(self):
        if not BlockChain.check_existing():
            initial_hash = hashlib.sha512("Pay with MarkusCoin!".encode()).hexdigest()
            self.construct_block(proof_no=1, previous_hash=initial_hash)
        else:
            self.construct_block(None, None)

    def construct_block(self, proof_no, previous_hash):
        if (proof_no is not None) and (previous_hash is not None):
            index = len(self.chain)
            data = self.current_data
            
            block = Block(
                index=index,
                proof_no=proof_no,
                previous_hash=previous_hash,
                transaction_data=data
            )

            self.current_data = []
            self.chain.append(block)

            BlockChain.add_payment(self)
        else:
            blockchain = BlockChain.get_blockchain()
            
            for block_data in blockchain:
                transaction = block_data['transaction']
                if len(transaction) == 3:
                    data = self.new_data(
                        sender=transaction.get('sender'),
                        recipient=transaction.get('recipient'),
                        quantity=transaction.get('quantity')
                    )

                block = Block(
                    index=block_data['index'],
                    proof_no=block_data['proof'],
                    previous_hash=block_data['previous_hash'],
                    transaction_data=self.current_data,
                    timestamp=block_data['timestamp']
                )

                if len(self.chain) >= 1:
                    check = BlockChain.check_validity(block, self.last_block)
                    if not check:
                        print('Es wurde eine Datenmanipulation erkannt!')
                        exit()

                self.current_data = []
                self.chain.append(block)

        return block

    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })

        return True

    # VERIFING THE BLOCK OR THE BLOCKCHAIN
    @staticmethod
    def check_validity(block, previous_block):
        if previous_block.index + 1 != block.index:
            return False

        elif previous_block.calculate_hash != block.previous_hash:
            return False

        elif not BlockChain.verifying_proof(block.proof_no, previous_block.proof_no):
            return False

        elif previous_block.timestamp >= block.timestamp:
            return False
        
        else:
            return True

    @staticmethod
    def proof_of_work(previous_proof):
        proof_no = 0

        while BlockChain.verifying_proof(proof_no, previous_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(previous_proof, proof):
        proof_value = '000000'
        secure_length = len(proof_value)

        guess = f'{previous_proof}{proof}'.encode()
        guess_hash = hashlib.sha512(guess).hexdigest()

        return guess_hash[0:secure_length] == proof_value
   
    @property
    def last_block(self):
        return self.chain[-1]

    # ADD THE NEW BLOCK TO JSON
    @staticmethod
    def check_existing():
        file_exist = False

        try:
            json_file = open('payments.json', 'r')
            file_exist = True

        except IOError:
            file_exist = False
            
        finally:
            if 'json_file' in locals() and json_file:
                json_file.close()
        
        return file_exist

    @staticmethod
    def get_blockchain():
        if BlockChain.check_existing():
            with open('payments.json', 'r') as json_file:
                blockchain = json.load(json_file)

            return blockchain

        else:
            return None
    
    @staticmethod
    def add_payment(self):
        tmp_data = []
        last_block = self.last_block

        try:
            if BlockChain.check_existing():
                with open('payments.json', 'r') as json_file:
                    tmp_data = json.load(json_file)

            if len(last_block.transaction_data) == 1:
                transaction = {
                    'sender': last_block.transaction_data[0].get('sender'),
                    'recipient': last_block.transaction_data[0].get('recipient'),
                    'quantity': last_block.transaction_data[0].get('quantity')
                }
            else:
                transaction = { }
            
            new_block = {
                'index': last_block.index,
                'proof': last_block.proof_no,
                'previous_hash': last_block.previous_hash,
                'transaction': transaction,
                'timestamp': last_block.timestamp
            }
            
            tmp_data.append(new_block)
            
            with open('payments.json', 'w') as json_file:
                json.dump(tmp_data, json_file, indent=4, ensure_ascii=False)

        except Exception as ex:
            print(ex)

    # MINING THE CRYPTOCURRENCY
    def block_mining(self, miner):
        self.new_data(
            sender="0",
            recipient=miner,
            quantity=1
        )

        last_block = self.last_block

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    def create_node(self, address):
        self.node.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['previous_has'],
            block_data['data'],
            timestamp=block_data['timestamp']
        )
