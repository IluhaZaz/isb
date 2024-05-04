from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class AsymmetricKey:

    def __init__(self):

        self.private_key = None
        self.public_key = None
    

    def generate_keys(self) -> None:

        keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        )

        self.private_key = keys
        self.public_key = keys.public_key()
    

    def serialize_keys(self, public_pem: str, private_pem: str, logger) -> bool:
        try:
            with open(public_pem, 'wb') as public_out:
                    public_out.write(self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except:
             logger.critical("Error while writing public key to file")
             return False

        try:
            with open(private_pem, 'wb') as private_out:
                    private_out.write(self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()))
            return True
        
        except:
            logger.critical("Error while writing private key to file")
            return False


    @staticmethod
    def deserialize_keys(public_pem: str, private_pem: str, logger) -> tuple[bytes, bytes]:
        try:
            with open(public_pem, 'rb') as pem_in:
                public_bytes = pem_in.read()
                public_key = load_pem_public_key(public_bytes)
        except:
            logger.critical("Error while reading public key from file")
            return None
        
        try:
            with open(private_pem, 'rb') as pem_in:
                private_bytes = pem_in.read()
                private_key = load_pem_private_key(private_bytes,password=None,)
                return (private_key, public_key)
        except:
            logger.critical("Error while reading private key from file")
            return None
        

    @staticmethod
    def encrypt_symm_key(key: bytes, public_key) -> bytes:
        res = public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                                        algorithm=hashes.SHA256(),label=None))
        return res
    

    @staticmethod
    def decrypt_symm_key(key: bytes, private_key) -> bytes:
        res = private_key.decrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                                          algorithm=hashes.SHA256(),label=None))
        return res