import os
import logging

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


from utils.io_to_file import read_bytes, write_bytes, write_to_file


class SymmetricKey:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.key = None

    
    def generate_key(self, key_byte_size: int = 16) -> bool:

        if not 4 <= key_byte_size <= 56:
            self.logger.error("Key size must be from 4 to 56 in bytes") 
            return False

        self.key = os.urandom(key_byte_size)
        return True
    

    def serialize_key(self, path: str) -> bool:
        try:
            write_bytes(path, self.key, self.logger)
            return True

        except Exception:
            self.logger.critical("Error while writing to file")

        return False


    def deserialize_key(self, path: str) -> bool:
        try:
            self.key = read_bytes(path, self.logger)
            return True

        except Exception:
            self.logger.critical("Error while reading file")

        return False
    

    def encrypt(self, text_path: str, encrypted_text_path: str) -> None:

        text = read_bytes(text_path)

        padder = padding.ANSIX923(16).padder()
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()

        write_bytes(encrypted_text_path, c_text, self.logger)

    
    def decrypt(self, text_path: str, decrypted_text_path: str) -> None:
        text = read_bytes(text_path)

        iv = text[:8]
        text = text[8:]

        cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        text = decryptor.update(text) + decryptor.finalize()
        unpadder = padding.ANSIX923(16).unpadder()
        unpadded_text = unpadder.update(text) + unpadder.finalize()
        text = unpadded_text.decode('UTF-8')

        write_to_file(decrypted_text_path, text, self.logger)
