from blockchain.block import Block
from blockchain.transaction import Transaction
from blockchain.blockchain import Blockchain
from datetime import datetime
import json
from sys import argv

blockchain = Blockchain()
names = ["Thaddeus", "Toledo", "Thaddeus", "Toledo"]
transactions = []
arguments = argv[1:]
SK = "f3575bb084fe0d0c46c42f92634794d2d12c48946222a726b69aa80449886fa2"
PK = "f93bbdda8c208a5d2723f2d6c236602b11c140abd8a19b1b91609679350a2cae9211063746de389ae5a5dbabd5283ece9d4d67c0dd8f14600bbaeb51476c972f"

# Create Transactions
if "--create-transactions" in arguments or len(arguments) == 0:
    for i in range(0, len(names)):
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        transaction = Transaction(names[i], index = i, private_key = SK)
        transactions.append(transaction)

# if "--show-transactions" in arguments or len(arguments) == 0:
#     for transaction in transactions:
#         print(transaction.validate_transaction())
#         print(transaction.transaction_values())

# Create Block
if "--create-block" in arguments or len(arguments) == 0:
    block = Block(transactions, blockchain.get_previous_block_hash(), index = blockchain.get_next_index())
    block.nonce = block.calculate_block_nonce()

    blockchain.add_block(block)

    print(f"System Generated Chain Validity: {blockchain.validate_chain()}")

if "--export" in arguments or len(arguments) == 0:
    blockchain.export_chain()

# Load the chain from the database
if "--import" in arguments or len(arguments) == 0:
    blockchain.import_chain("blockchain")
    print(f"Database Generated Chain Validity: {blockchain.validate_chain()}")