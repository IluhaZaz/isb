import logging

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class AsymmetricKey:

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.private_key = None
        self.public_key = None
    

    def generate_keys(self) -> None:

        keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        )

        self.private_key = keys
        self.public_key = keys.public_key()
    

    def serialize_key(self, public_pem: str, private_pem: str) -> bool:
        try:
            with open(public_pem, 'wb') as public_out:
                    public_out.write(self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except:
             self.logger.critical("Error while writing public key to file")
             return False

        try:
            with open(private_pem, 'wb') as private_out:
                    private_out.write(self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()))
            return True
        
        except:
            self.logger.critical("Error while writing private key to file")
            return False
