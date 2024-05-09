import os
import logging


class SymmetricKey:

    def __init__(self):
        self.key = None

    
    def generate_key(self, logger: logging.Logger, key_byte_size: int = 16) -> bool:

        """Generates key for Blowfish algorithm"""

        if not 4 <= key_byte_size <= 56:
            logger.error("Key size must be from 4 to 56 in bytes") 
            return False

        self.key = os.urandom(key_byte_size)
        return True
