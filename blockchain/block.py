from hashlib import sha256
from . import config

class Block:

    def __init__(self, transactions: list = None, previous_block_hash: str = None, nonce: int = None, root_hash: str = None, block_hash: str = None, index: int = None) -> None:
        
        self.previous_block_hash = previous_block_hash
        self.nonce = nonce
        self.index = index
        num_transactions = len(transactions)

        if num_transactions <= 0:
            print(num_transactions)
            raise ValueError("Invalid number of transactions in the block")
        if (num_transactions & (num_transactions - 1)) != 0 and num_transactions != 1:
            raise ValueError("Invalid number of transactions. The number of transactions must be a power of 2")
        else:
            self.transactions = transactions

        if root_hash is None:
            self.root_hash = self.calculate_root_hash()
        else:
            self.root_hash = root_hash

        if block_hash is None:
            self.block_hash = self.calculate_block_hash()
        else:
            self.block_hash = block_hash

    def calculate_root_hash(self) -> str:
        def root_hash(transactions):
            if len(transactions) == 1:
                return transactions[0]
            new_level = []
            for i in range(0, len(transactions), 2):
                new_hash = sha256((transactions[i] + transactions[i + 1]).encode()).hexdigest()
                new_level.append(new_hash)
            return root_hash(new_level)
        
        transaction_hashes = [transaction.transaction_hash for transaction in self.transactions]
        calculated_root_hash = root_hash(transaction_hashes)
        return calculated_root_hash
    
    def calculate_block_hash(self) -> str:
        data = (str(self.root_hash) + str(self.previous_block_hash)).encode()
        calculated_block_hash = sha256(data).hexdigest()
        return calculated_block_hash
    
    def calculate_block_nonce(self) -> int:
        print(f"Mining block for index {self.index}")
        combined_hash = sha256(str(self.index).encode() + self.block_hash.encode() + self.previous_block_hash.encode() + self.root_hash.encode()).hexdigest()
        nonce = 0
        while True:
            nonce_hash = sha256((combined_hash + str(nonce)).encode()).hexdigest()
            if nonce_hash.startswith("0" * config()['num_zeros']):
                break
            nonce += 1
        return nonce
    
    def block_values(self) -> dict:
        return {
            "index": self.index,
            "block_hash": self.block_hash,
            "previous_block_hash": self.previous_block_hash,
            "nonce": self.nonce,
            "root_hash": self.root_hash,
            "transactions": [transaction.transaction_values() for transaction in self.transactions]
        }

    def validate_block(self, previous_block_hash, index) -> bool:
        if self.index != index:
            print(f"Invalid Index: {self.index} != {index}")
            return False
        
        if self.previous_block_hash != previous_block_hash:
            print(f"Invalid Previous Block Hash: {self.previous_block_hash} != {previous_block_hash}")
            return False
        
        if self.block_hash != self.calculate_block_hash():
            print(f"Invalid Block Hash: {self.block_hash} != {self.calculate_block_hash()}")
            return False
        
        if self.root_hash != self.calculate_root_hash():
            print(f"Invalid Root Hash: {self.root_hash} != {self.calculate_root_hash()}")
            return False
        
        if sha256(str(self.index).encode() + self.block_hash.encode() + self.previous_block_hash.encode() + self.root_hash.encode()).hexdigest().startswith("0" * config()['num_zeros']) == False:
            print(f"Invalid Nonce: {self.nonce}")
            return False

        return True