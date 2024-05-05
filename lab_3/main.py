import argparse
import logging

from classes.asymmetric import AsymmetricKey
from classes.symmetric import SymmetricKey

from classes.utils.io_to_file import read_json, write_bytes, read_bytes


def keys_generation(symmetric: SymmetricKey, asymmetric: AsymmetricKey, 
                    paths: dict[str, str], logger: logging.Logger, symm_key_size: int = 16):

    symmetric.generate_key(symm_key_size)
    asymmetric.generate_keys()

    asymmetric.serialize_keys(paths["public_key"], paths["private_key"], logger)

    encrypted = asymmetric.encrypt_symm_key(symmetric.key, asymmetric.public_key)

    write_bytes(paths["encrypted_symm_key"], encrypted, logger)
    write_bytes(paths["decrypted_symm_key"], symmetric.key, logger)


def encrypt_data(text_path: str, private_key_path: str, enc_symm_key_path: str, 
                 enc_text_path: str, logger: logging.Logger):
    
    enc_symm_key = read_bytes(enc_symm_key_path, logger)
    private_key = read_bytes(private_key_path, logger)
    private_key = AsymmetricKey.deserialize_keys(paths["public_key"], paths["private_key"], logger)[0]
    symm_key = AsymmetricKey.decrypt_symm_key(enc_symm_key, private_key)

    SymmetricKey.encrypt(text_path, enc_text_path, symm_key, logger)


def decrypt_data(enc_text_path: str, private_key_path: str, enc_symm_key_path: str, 
                 text_path: str, logger: logging.Logger):
    
    enc_symm_key = read_bytes(enc_symm_key_path, logger)
    private_key = read_bytes(private_key_path, logger)
    private_key = AsymmetricKey.deserialize_keys(paths["public_key"], paths["private_key"], logger)[0]
    symm_key = AsymmetricKey.decrypt_symm_key(enc_symm_key, private_key)

    SymmetricKey.decrypt(enc_text_path, text_path, symm_key, logger)


if __name__ == "__main__":

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{')

    logger = logging.getLogger(__name__)

    paths = read_json("settings.json", logger)

    symmetric = SymmetricKey()
    asymmetric = AsymmetricKey()

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation', help='Starts key generation mode', action="store_true")
    group.add_argument('-enc','--encryption', help='Starts encryption mode', action="store_true")
    group.add_argument('-dec','--decryption', help='Starts decrypyion mode', action="store_true")

    parser.add_argument('-k', '--key_byte_size', type = int, default = 16, help = 'Size of symmetric key in bytes')

    args = parser.parse_args()

    if args.generation is not None:
        keys_generation(symmetric, asymmetric, paths, logger, args.key_byte_size)
    elif args.encryption is not None:
        encrypt_data(paths["text"], paths["private_key"], paths["encrypted_symm_key"], paths["encrypted_text"], logger)
    else:
        decrypt_data(paths["encrypted_text"], paths["private_key"], paths["encrypted_symm_key"], paths["decrypted_text"], logger)
    #python main.py -gen -k 16
    #python main.py -enc
    #python main.py -dec