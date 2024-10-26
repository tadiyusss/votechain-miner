from hashlib import sha256
from blockchain.storage import StorageManager
from . import config

class Blockchain:
    
    def __init__(self) -> None:
        self.chain = []
    
    def add_block(self, block) -> None:
        self.chain.append(block)

    def get_next_index(self) -> int:
        return len(self.chain)
    
    def get_previous_block_hash(self) -> str:
        if len(self.chain) == 0:
            return "0"
        return self.chain[-1].block_hash

    def validate_chain(self) -> bool:
        for iterator in range(0, len(self.chain)):
            
            current_block = self.chain[iterator]
            previous_block = self.chain[iterator - 1]

            # Index   
            if current_block.index != iterator:
                print(f"Block {iterator} has an invalid index")
                return False

            # Previous block hash
            if current_block.previous_block_hash != previous_block.block_hash:
                if iterator != 0:
                    print(f"Block {iterator} has an invalid previous block hash")
                    return False

            # Current block hash    
            if current_block.block_hash != current_block.calculate_block_hash():
                print(f"Block {iterator} has an invalid block hash")
                return False
            
            # Root hash
            if current_block.root_hash != current_block.calculate_root_hash():
                print(f"Block {iterator} has an invalid root hash")
                return False

            # Nonce
            combined_hash = sha256(str(current_block.index).encode() + current_block.block_hash.encode() + current_block.previous_block_hash.encode() + current_block.root_hash.encode()).hexdigest()
            if sha256((combined_hash + str(current_block.nonce)).encode()).hexdigest().startswith("0" * config()['num_zeros']) == False:
                print(f"Block {iterator} has an invalid nonce")
                return False

            # Transactions
            for transaction_iterator in range(0, len(current_block.transactions)):
                transaction = current_block.transactions[transaction_iterator]

                if transaction.index != transaction_iterator:
                    print(f"Block {iterator} has an invalid transaction index")
                    return False
                
                if transaction.validate_transaction() == False:
                    print(f"Block {iterator} has an invalid transaction")
                    return False
                
        return True

    def export_chain(self, filename = "blockchain"):
        storage_manager = StorageManager(f"{filename}.db")
        db_chain_length = storage_manager.get_chain_length()

        for i in range(db_chain_length, len(self.chain)):
            block = self.chain[i]
            storage_manager.save_block(block)
            for transaction in block.transactions:
                print(transaction)
                storage_manager.save_transaction(transaction, block.block_hash)
        
        storage_manager.close()

    def import_chain(self, filename):
        storage_manager = StorageManager(f"{filename}.db")
        db_chain_length = storage_manager.get_chain_length()
        ram_chain_length = len(self.chain)

        for i in range(ram_chain_length, db_chain_length):
            block_values = storage_manager.view_block_by_index(i)
            transactions = storage_manager.view_transactions_by_block_hash(block_values["block_hash"])
            transactions = [storage_manager.transaction_dict_to_obj(transaction) for transaction in transactions]
            block_obj = storage_manager.block_dict_to_obj(block_values, transactions)
            self.chain.append(block_obj)
        return self.chain