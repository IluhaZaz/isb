import json
import logging

from logging import Logger
from typing import Dict
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import rsa


class FileHandler:

    @staticmethod
    def read_bytes(file: str, logger: Logger) -> bytes:
        res = b''
        try:
            with open(file, 'rb') as f:
                res = f.read()
        except:
            logger.critical("Can't open input file")
        return res


    @staticmethod
    def write_bytes(path: str, text: bytes, logger: Logger) -> None:

        try:
            with open(path, "wb") as file:
                file.write(text)
        except Exception:
            logger.critical("Can't open output json file")


    @staticmethod
    def read_file(file: str, logger: Logger) -> str:
        res = ""
        try:
            with open(file, mode = "r", encoding = "utf-8") as f:
                res = f.read()
        except:
            logger.critical("Can't open input file")
        return res


    @staticmethod
    def write_to_file(file: str, text: str, logger: Logger) -> None:
        try:
            with open(file, mode = "w", encoding = "utf-8") as f:
                f.write(text)
        except:
            logger.critical("Can't open output file")


    @staticmethod
    def write_to_json(d: Dict[str, str], file: str, logger: Logger) -> None:
        try:
            with open(file, mode = "w", encoding = "utf-8") as f:
                json.dump(d, f, ensure_ascii = False, indent=4)
        except:
            logger.critical("Can't open output json file")


    @staticmethod
    def read_json(file: str, logger: Logger) -> Dict[str, str]:
        try:
            with open(file, mode = "r", encoding = "utf-8") as f:
                return json.loads(f.read())
        except:
            logger.critical("Can't open input json file")
            return {}
    

    @staticmethod
    def serialize_asymmetric_keys(public_key: rsa.RSAPublicKey, private_key: rsa.RSAPrivateKey, 
                       public_pem: str, private_pem: str, logger: logging.Logger) -> bool:

        """Serializes RSA's keys"""

        FileHandler.write_bytes(public_pem, public_key.public_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo), logger)
            
        FileHandler.write_bytes(private_pem, private_key.private_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()), logger)


    @staticmethod
    def deserialize_asymmetric_keys(public_pem: str, private_pem: str, logger: logging.Logger) -> tuple[bytes, bytes]:

        """Deserializes RSA's keys"""

        public_bytes = FileHandler.read_bytes(public_pem, logger)
        public_key = load_pem_public_key(public_bytes)

        private_bytes = FileHandler.read_bytes(private_pem, logger)
        private_key = load_pem_private_key(private_bytes,password=None,)

        return (private_key, public_key)


    @staticmethod
    def serialize_symmetric_key(path: str, key: bytes, logger: logging.Logger) -> bool:

            """Serializes Blowfish's key"""

            try:
                FileHandler.write_bytes(path, key, logger)
                return True

            except Exception:
                logger.critical("Error while writing to file")

            return False


    @staticmethod
    def deserialize_symmetric_key(path: str, logger: logging.Logger) -> bytes:

        """Deserializes Blowfish's key"""

        try:
            key = FileHandler.read_bytes(path, logger)
            return key

        except Exception:
            logger.critical("Error while reading file")

        return None
    