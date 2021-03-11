import hashlib, json, time


class Block():
    def __init__(self, index, proof_no, previous_hash, transaction_data, timestamp=None):
        self.index = index
        self.proof_no = proof_no
        self.previous_hash = previous_hash
        self.transaction_data = transaction_data
        self.timestamp = timestamp or time.time()
    
    @property
    def calculate_hash(self):
        block_of_string = "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
                                                          self.previous_hash, self.transaction_data,
                                                          self.timestamp)

        return hashlib.sha512(block_of_string.encode()).hexdigest()

    def __repr__(self):
        output = {
            'index': self.index,
            'proof': self.proof_no,
            'previous_hash': self.previous_hash,
            'transaction': self.transaction_data,
            'time_stamp': self.timestamp
        }
    
        return json.dumps(output, indent=4, ensure_ascii=False)
