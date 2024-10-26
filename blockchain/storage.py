import sqlite3
from .block import Block
from .transaction import Transaction

class StorageManager:
    def __init__(self, database_name) -> None:
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS `blocks` (`block_index` INT NOT NULL, `block_hash` VARCHAR(64) NOT NULL , `previous_block_hash` VARCHAR(64) NOT NULL , `root_hash` VARCHAR(64) NOT NULL , `nonce` INT NOT NULL );")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS `transactions` (`transaction_index` INT NOT NULL , `data` VARCHAR(255) NOT NULL , `timestamp` VARCHAR(255) NOT NULL , `transaction_hash` VARCHAR(64) NOT NULL , `block_hash` VARCHAR(64) NOT NULL, `public_key` VARCHAR(128) NOT NULL, `signature` VARCHAR(128) NOT NULL );")

    def save_block(self, block: Block = None) -> None:
        self.cursor.execute("INSERT INTO blocks VALUES (?, ?, ?, ?, ?)", (block.index, block.block_hash, block.previous_block_hash, block.root_hash, block.nonce))
        self.connection.commit()
    
    def save_transaction(self, transaction: Transaction = None, block_hash: str = None) -> None:
        self.cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)", (transaction.index, transaction.data, transaction.timestamp, transaction.transaction_hash, block_hash, transaction.public_key, transaction.signature))
        self.connection.commit()
    
    def view_block(self, block_hash: str = None) -> dict | None:
        if block_hash:
            self.cursor.execute("SELECT * FROM blocks WHERE block_hash = ?", (block_hash,))
            block = self.cursor.fetchone()
            return self.format_block_sql_result(block)
        else:
            return None
    
    def view_transaction(self, block_hash: str = None, transaction_hash: str = None) -> dict | None:
        if block_hash and transaction_hash:
            
            self.cursor.execute("SELECT * FROM transactions WHERE block_hash = ? AND transaction_hash = ?", (block_hash, transaction_hash))
            transaction = self.cursor.fetchone()

            return self.format_transaction_sql_result(transaction)
        
        else:
            return None
    
    def view_block_by_index(self, index: int = None) -> dict | None:
        if index != None:
            self.cursor.execute("SELECT * FROM blocks WHERE block_index = ?", (index,))
            block = self.cursor.fetchone()
            return self.format_block_sql_result(block)
        else:
            return None

    def format_block_sql_result(self, block) -> dict:
        return {
            "index": block[0],
            "block_hash": block[1],
            "previous_block_hash": block[2],
            "root_hash": block[3],
            "nonce": block[4]
        }
    
    def format_transaction_sql_result(self, transaction) -> dict:
        return {
            "index": transaction[0],
            "data": transaction[1],
            "timestamp": transaction[2],
            "transaction_hash": transaction[3],
            "block_hash": transaction[4],
            "public_key": transaction[5],
            "signature": transaction[6]
        }

    def block_dict_to_obj(self, block: dict, transactions: list[Transaction]) -> Block:
        return Block(
            transactions = transactions,
            index = block["index"],
            block_hash = block["block_hash"],
            previous_block_hash = block["previous_block_hash"],
            root_hash = block["root_hash"],
            nonce = block["nonce"]
        )
    
    def transaction_dict_to_obj(self, transaction: dict) -> Transaction:
        return Transaction(
            data = transaction["data"],
            index = transaction["index"],
            timestamp = transaction["timestamp"],
            transaction_hash = transaction["transaction_hash"],
            public_key = transaction["public_key"],
            signature = transaction["signature"]
        )

    def view_transactions_by_public_key(self, public_key: str = None) -> list | None:
        if public_key:
            
            self.cursor.execute("SELECT * FROM transactions WHERE public_key = ?", (public_key,))
            transactions = self.cursor.fetchall()
            results = [self.format_transaction_sql_result(transaction) for transaction in transactions]
            return results
        else:
            return None
    
    def view_transactions_by_block_hash(self, block_hash: str = None) -> list | None:
        if block_hash:
            self.cursor.execute("SELECT * FROM transactions WHERE block_hash = ?", (block_hash,))
            transactions = self.cursor.fetchall()
            results = [self.format_transaction_sql_result(transaction) for transaction in transactions]
            return results
        else:
            return None

    def get_chain_length(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM blocks")
        return self.cursor.fetchone()[0]

    def close(self) -> None:
        self.connection.close()