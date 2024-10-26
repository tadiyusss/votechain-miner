from hashlib import sha256
from datetime import datetime
from .keys import Keys

class Transaction:
    def __init__(self, data = None, timestamp = None, transaction_hash = None, index = None, private_key: str = None, public_key: str = None, signature: str = None) -> None:
        keys = Keys()
        self.data = data
        self.index = index

        if private_key is None and public_key is None:
            raise ValueError("Either private_key or public_key must be provided.")
        
        if public_key is None:
            self.public_key = keys.get_public_key(private_key)
        else:
            self.public_key = public_key

        if timestamp is None:
            self.timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        else:
            self.timestamp = timestamp

        if transaction_hash is None:
            self.transaction_hash = self.calculate_transaction_hash()
        else:
            self.transaction_hash = transaction_hash
        
        if signature is None:
            self.signature = keys.sign(private_key, str(self.transaction_hash) + str(self.public_key))
        else:
            self.signature = signature

    def calculate_transaction_hash(self) -> None:
        data = (str(self.data) + str(self.timestamp) + str(self.public_key) + str(self.index)).encode()
        return sha256(data).hexdigest()
    
    def transaction_values(self) -> dict:
        return self.__dict__
    
    def validate_transaction(self) -> bool:
        keys = Keys()

        # Check Hash
        if self.transaction_hash != self.calculate_transaction_hash():
            print(f"Invalid Hash: {self.transaction_hash} != {self.calculate_transaction_hash()}")
            return False
        
        # Check Signature
        if keys.verify(self.public_key, self.signature, str(self.transaction_hash) + str(self.public_key)) == False:
            print(f"Invalid Signature: {self.signature}")
            return False
        
        # Check Timestamp
        if datetime.strptime(self.timestamp, "%m/%d/%Y %H:%M:%S") > datetime.now():
            print(f"Invalid Timestamp: {self.timestamp}")
            return False
        
        # Check Index
        if self.index is None:
            print(f"Invalid Index: {self.index}")
            return False

        return True