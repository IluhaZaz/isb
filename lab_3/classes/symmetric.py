import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from utils.io_to_file import read_bytes, write_bytes


class SymmetricKey:

    def __init__(self):
        self.key = None

    
    def generate_key(self, key_byte_size: int) -> bytes:

        if not 4 <= key_byte_size <= 56:
            raise ValueError("Key size must be from 4 to 56 in bytes") 

        self.key = os.urandom(key_byte_size)

        return self.key
    

    def serialize_key(self, path: str) -> bool:
        try:
            with open(path, 'wb') as file:
                file.write(self.key)
            return True

        except Exception:
            print("Error while writing to file")

        return False


    def deserialize_key(self, path: str) -> bool:
        try:
            with open(path, 'rb') as file:
                file.read(self.key)
            return True

        except Exception:
            print("Error while reading file")

        return False
    

    def encrypt(self, text_path: str, encrypted_text_path: str) -> bool:

        text = read_bytes(text_path)

        padder = padding.ANSIX923(16).padder()
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()

        write_bytes(encrypted_text_path, c_text)
