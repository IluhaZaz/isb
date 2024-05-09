from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class AsymmetricKey:

    def __init__(self):

        self.private_key = None
        self.public_key = None
    

    def generate_keys(self) -> None:

        """Generates keys for RSA algorithm"""

        keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        )

        self.private_key = keys
        self.public_key = keys.public_key()
        

    @staticmethod
    def encrypt_symm_key(key: bytes, public_key: rsa.RSAPublicKey) -> bytes:

        """Encrypts symmetric key"""

        res = public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                                        algorithm=hashes.SHA256(),label=None))
        return res
    

    @staticmethod
    def decrypt_symm_key(key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:

        """Decrypts symmetric key"""

        res = private_key.decrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                                          algorithm=hashes.SHA256(),label=None))
        return res
    