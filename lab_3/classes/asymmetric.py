import logging

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from classes.io_to_file import read_bytes, write_bytes


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
    

    def serialize_keys(self, public_pem: str, private_pem: str, logger: logging.Logger) -> bool:

        """Serializes RSA's keys"""

        write_bytes(public_pem, self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo), logger)
        
        write_bytes(private_pem, self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()), logger)


    @staticmethod
    def deserialize_keys(public_pem: str, private_pem: str, logger: logging.Logger) -> tuple[bytes, bytes]:

        """Deserializes RSA's keys"""

        public_bytes = read_bytes(public_pem, logger)
        public_key = load_pem_public_key(public_bytes)

        private_bytes = read_bytes(private_pem, logger)
        private_key = load_pem_private_key(private_bytes,password=None,)

        return (private_key, public_key)
        

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
    