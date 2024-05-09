import os
import logging

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from classes.symmetric import SymmetricKey
from classes.asymmetric import AsymmetricKey
from classes.io_to_file import FileHandler


class HybridCryptoSystem:

    def __init__(self) -> None:

        self.symmetric_key = SymmetricKey()
        self.asymmetric_key = AsymmetricKey()
    

    @staticmethod
    def encrypt(text_path: str, encrypted_text_path: str, key: bytes, logger: logging.Logger) -> None:

        "Encrypts text with Blowfish algorothm"

        text = FileHandler.read_bytes(text_path, logger)

        padder = padding.ANSIX923(128).padder()
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = iv + encryptor.update(padded_text) + encryptor.finalize()

        FileHandler.write_bytes(encrypted_text_path, c_text, logger)

    
    @staticmethod
    def decrypt(text_path: str, decrypted_text_path: str, key: bytes, logger: logging.Logger) -> None:

        "Decrypts text with Blowfish algorothm"

        text = FileHandler.read_bytes(text_path, logger)

        iv = text[:8]
        text = text[8:]

        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        text = decryptor.update(text) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_text = unpadder.update(text) + unpadder.finalize()
        text = unpadded_text.decode('UTF-8')

        FileHandler.write_to_file(decrypted_text_path, text, logger)


    def keys_generation(self, paths: dict[str, str], logger: logging.Logger, symm_key_size: int = 16):
    
        """Generates keys for both symmetric and aymetric algorithms"""

        self.symmetric_key.generate_key(symm_key_size)
        self.asymmetric_key.generate_keys()

        FileHandler.serialize_asymmetric_keys(self.asymmetric_key.public_key, self.asymmetric_key.private_key, 
                                              paths["public_key"], paths["private_key"], logger)

        encrypted = AsymmetricKey.encrypt_symm_key(self.symmetric_key.key, self.asymmetric_key.public_key)

        FileHandler.write_bytes(paths["encrypted_symm_key"], encrypted, logger)
        FileHandler.write_bytes(paths["decrypted_symm_key"], self.symmetric_key.key, logger)


    @staticmethod
    def encrypt_data(paths: dict[str, str], logger: logging.Logger):
    
        """Encrypts provided data"""
        
        enc_symm_key = FileHandler.read_bytes(paths["encrypted_symm_key"], logger)
        private_key = FileHandler.read_bytes(paths["private_key"], logger)
        private_key = FileHandler.deserialize_asymmetric_keys(paths["public_key"], paths["private_key"], logger)[0]
        symm_key = AsymmetricKey.decrypt_symm_key(enc_symm_key, private_key)

        HybridCryptoSystem.encrypt(paths["text"], paths["encrypted_text"], symm_key, logger)
    

    @staticmethod
    def decrypt_data(paths: dict[str, str], logger: logging.Logger):
    
        """Decrypts provided data"""
        
        enc_symm_key = FileHandler.read_bytes(paths["encrypted_symm_key"], logger)
        private_key = FileHandler.read_bytes(paths["private_key"], logger)
        private_key = FileHandler.deserialize_asymmetric_keys(paths["public_key"], paths["private_key"], logger)[0]
        symm_key = AsymmetricKey.decrypt_symm_key(enc_symm_key, private_key)

        HybridCryptoSystem.decrypt(paths["encrypted_text"], paths["decrypted_text"], symm_key, logger)
        