
from ecdsa import SigningKey, SECP256k1, VerifyingKey

class Keys:
    def __init__(self):
        pass

    def generate_keys(self) -> dict:
        private_key = SigningKey.generate(curve = SECP256k1)
        public_key = private_key.get_verifying_key()
        return {
            "private_key": private_key.to_string().hex(),
            "public_key": public_key.to_string().hex()
        }

    def get_public_key(self, private_key: str) -> str:
        private_key = bytes.fromhex(private_key)
        private_key = SigningKey.from_string(private_key, curve = SECP256k1)
        public_key = private_key.get_verifying_key()
        return public_key.to_string().hex()
    
    def sign(self, private_key: str, message: str) -> str:
        private_key = bytes.fromhex(private_key)
        private_key = SigningKey.from_string(private_key, curve = SECP256k1)
        signature = private_key.sign(message.encode())
        return signature.hex()

    def verify(self, public_key: str, signature: str, message: str) -> bool:
        public_key = bytes.fromhex(public_key)
        public_key = VerifyingKey.from_string(public_key, curve = SECP256k1)
        signature = bytes.fromhex(signature)
        return public_key.verify(signature, message.encode())
