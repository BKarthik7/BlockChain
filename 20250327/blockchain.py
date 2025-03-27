# blockchain.py

import time
import hashlib
import json

def computehash(block_header, previous_block_hash, nounce, block_data, timestamp):
    block_string = json.dumps({
        'block_header': block_header,
        'previous_block_hash': previous_block_hash,
        'nounce': nounce,
        'block_data': block_data,
        'timestamp': timestamp
    }, sort_keys=True).encode()
    
    return hashlib.sha256(block_string).hexdigest()

class Block:
    def __init__(self, block_header, previous_block_hash, nounce, block_data):
        self.block_header = block_header
        self.previous_block_hash = previous_block_hash
        self.timestamp = time.time() 
        self.nounce = nounce
        self.block_data = block_data
        self.block_data_hash = computehash(block_header, previous_block_hash, nounce, block_data, self.timestamp)
        self.data = block_data  

    def __repr__(self):
        return f"Block(header={self.block_header}, previous_hash={self.previous_block_hash}, nounce={self.nounce}, data={self.block_data}, timestamp={self.timestamp}, hash={self.block_data_hash})"

class Transaction:
    def __init__(self, sender, receiver, amount, description):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"Transaction(sender={self.sender}, receiver={self.receiver}, amount={self.amount}, description={self.description})"

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [] 
        self.difficulty = difficulty 
        self.create_genesis_block() 

    def create_genesis_block(self):
        genesis_block = Block(block_header="Genesis Block", previous_block_hash="0", nounce=0, block_data={"message": "This is the genesis block."})
        self.chain.append(genesis_block)

    def new_block(self, block_header, block_data):
        if not isinstance(block_data, dict):
            raise ValueError("block_data must be a dictionary. Received: " + str(type(block_data)))
        previous_block_hash = self.chain[-1].block_data_hash
        nounce = 0 
        timestamp = time.time()

        new_block = Block(block_header, previous_block_hash, nounce, block_data)

        while not new_block.block_data_hash.startswith('0' * self.difficulty):
            nounce += 1
            new_block.nounce = nounce
            new_block.block_data_hash = computehash(block_header, previous_block_hash, nounce, block_data, timestamp)

        self.chain.append(new_block)

    def add_transaction(self, sender, receiver, amount, description):
        transaction = Transaction(sender, receiver, amount, description)
        if isinstance(self.chain[-1].block_data, dict):
            self.chain[-1].block_data.setdefault("transactions", []).append(transaction)
        else:
            raise ValueError("Last block's data is not a dictionary")
        return transaction

    def get_balance(self, user):
        balance = 0
        for block in self.chain:
            if isinstance(block.block_data, dict):
                if block.block_data.get("receiver") == user:
                    balance += block.block_data.get("amount", 0)
                if block.block_data.get("sender") == user:
                    balance -= block.block_data.get("amount", 0)
        return balance

    def update_balance(self, user, amount):
        transaction = {
            "sender": "system",
            "receiver": user,
            "amount": amount,
            "description": "Balance update"
        }
        if isinstance(self.chain[-1].block_data, dict):
            self.chain[-1].block_data.setdefault("transactions", []).append(transaction)
        else:
            raise ValueError("Last block's data is not a dictionary")

    def __repr__(self):
        return f"Blockchain(chain={self.chain})"
