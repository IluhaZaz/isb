import argparse
import logging

from classes.asymmetric import AsymmetricKey
from classes.symmetric import SymmetricKey

from classes.io_to_file import read_json, write_bytes, read_bytes


def keys_generation(symmetric: SymmetricKey, asymmetric: AsymmetricKey, 
                    paths: dict[str, str], logger: logging.Logger, symm_key_size: int = 16):
    
    """Generates keys for both symmetric and aymetric algorithms"""

    symmetric.generate_key(symm_key_size)
    asymmetric.generate_keys()

    asymmetric.serialize_keys(paths["public_key"], paths["private_key"], logger)

    encrypted = asymmetric.encrypt_symm_key(symmetric.key, asymmetric.public_key)

    write_bytes(paths["encrypted_symm_key"], encrypted, logger)
    write_bytes(paths["decrypted_symm_key"], symmetric.key, logger)


def encrypt_data(paths: dict[str, str], logger: logging.Logger):
    
    """Encrypts provided data"""
    
    enc_symm_key = read_bytes(paths["encrypted_symm_key"], logger)
    private_key = read_bytes(paths["private_key"], logger)
    private_key = AsymmetricKey.deserialize_keys(paths["public_key"], paths["private_key"], logger)[0]
    symm_key = AsymmetricKey.decrypt_symm_key(enc_symm_key, private_key)

    SymmetricKey.encrypt(paths["text"], paths["encrypted_text"], symm_key, logger)


def decrypt_data(paths: dict[str, str], logger: logging.Logger):
    
    """Decrypts provided data"""
    
    enc_symm_key = read_bytes(paths["encrypted_symm_key"], logger)
    private_key = read_bytes(paths["private_key"], logger)
    private_key = AsymmetricKey.deserialize_keys(paths["public_key"], paths["private_key"], logger)[0]
    symm_key = AsymmetricKey.decrypt_symm_key(enc_symm_key, private_key)

    SymmetricKey.decrypt(paths["encrypted_text"], paths["decrypted_text"], symm_key, logger)


if __name__ == "__main__":

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{')

    logger = logging.getLogger(__name__)

    symmetric = SymmetricKey()
    asymmetric = AsymmetricKey()

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation', help='Starts key generation mode', action="store_true")
    group.add_argument('-enc','--encryption', help='Starts encryption mode', action="store_true")
    group.add_argument('-dec','--decryption', help='Starts decrypyion mode', action="store_true")

    parser.add_argument('-p', '--paths', type = str, help = 'Path to json file with paths')

    parser.add_argument('-k', '--key_byte_size', type = int, default = 16, help = 'Size of symmetric key in bytes')

    args = parser.parse_args()

    paths = read_json(args.paths, logger)

    if args.generation is not None:
        keys_generation(symmetric, asymmetric, paths, logger, args.key_byte_size)
    elif args.encryption is not None:
        encrypt_data(paths, logger)
    else:
        decrypt_data(paths, logger)
    #python main.py -gen -p settings.json -k 16
    #python main.py -enc -p settings.json
    #python main.py -dec -p settings.json