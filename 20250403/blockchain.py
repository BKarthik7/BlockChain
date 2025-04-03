import time
import hashlib
from cbc import encrypt_cbc, decrypt_cbc

block_size = 8
initial_vector = "initialy"

class Block:
    def __init__(self, block_header, previous_block_hash, nounce, block_data):
        self.block_header = block_header
        self.previous_block_hash = previous_block_hash
        self.timestamp = time.time()
        self.nounce = nounce
        self.block_data = encrypt_cbc(block_data, initial_vector, block_size)
        self.block_data_hash = self.computehash()

    def computehash(self):
        block_string = f"{self.block_header}{self.previous_block_hash}{self.nounce}{self.block_data}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_decrypted_data(self):
        decrypted_data = decrypt_cbc(self.block_data, initial_vector, block_size)
        print(f"Encrypted: {self.block_data}")
        print(f"Decrypted: {decrypted_data}")
        return decrypted_data

    def __repr__(self):
        return f"Block(header={self.block_header}, previous_hash={self.previous_block_hash}, nounce={self.nounce}, data={self.get_decrypted_data()}, timestamp={self.timestamp}, hash={self.block_data_hash})"

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("Genesis Block", "0", 0, "This is the genesis block.")
        self.chain.append(genesis_block)

    def new_block(self, block_header, block_data):
        previous_block_hash = self.chain[-1].block_data_hash
        nounce = 0

        new_block = Block(block_header, previous_block_hash, nounce, block_data)

        while not new_block.block_data_hash.startswith('0' * self.difficulty):
            nounce += 1
            new_block.nounce = nounce
            new_block.block_data_hash = new_block.computehash()

        self.chain.append(new_block)

    def __repr__(self):
        return f"Blockchain(chain={self.chain})"

if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.new_block("Block 1", "This is the first block.")
    blockchain.new_block("Block 2", "This is the second block.")

    print("----------------------------------------")

    print(blockchain)
