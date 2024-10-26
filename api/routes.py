from . import api
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.storage import StorageManager
from blockchain.transaction import Transaction
from os import path
from flask import request


blockchain = Blockchain()
pending_transactions = []


if path.exists("blockchain.db"):
    blockchain.import_chain("blockchain")

@api.route('/view/chain')
def view_chain():
    return {
        "blocks": [block.block_values() for block in blockchain.chain]
    }

@api.route('/view/chain/validity')
def view_chain_validity():
    return {
        "valid": blockchain.validate_chain()
    }

@api.route('/create/transaction', methods=['POST'])
def create_transaction():
    required_fields = ['data', 'private_key']
    if not all([field in request.json for field in required_fields]):
        return {
            "error": f"Incomplete transaction data. Required fields: {required_fields}"
        }
    values = {
        "data": request.json['data'],
        "private_key": request.json['private_key']
    }
    transaction = Transaction(values['data'], private_key = values['private_key'])