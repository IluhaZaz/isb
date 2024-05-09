import argparse
import logging

from classes.crypto_system import HybridCryptoSystem

from classes.io_to_file import FileHandler


if __name__ == "__main__":

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{')

    logger = logging.getLogger(__name__)

    system = HybridCryptoSystem()

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-gen','--generation', help='Starts key generation mode', action="store_true")
    group.add_argument('-enc','--encryption', help='Starts encryption mode', action="store_true")
    group.add_argument('-dec','--decryption', help='Starts decrypyion mode', action="store_true")

    parser.add_argument('-p', '--paths', type = str, help = 'Path to json file with paths')

    parser.add_argument('-k', '--key_byte_size', type = int, default = 16, help = 'Size of symmetric key in bytes')

    parser.add_argument('-ch', '--change_path', type = str, help = 'Change path to files/keys')

    args = parser.parse_args()

    paths = FileHandler.read_json(args.paths, logger)

    if args.change_path:
        temp = args.change_path.split(",")

        if temp[0] in paths.keys():
            paths[temp[0]] = temp[1]

    if args.generation is not None:
        system.keys_generation(paths, logger, args.key_byte_size)
    elif args.encryption is not None:
        HybridCryptoSystem.encrypt_data(paths, logger)
    else:
        HybridCryptoSystem.decrypt_data(paths, logger)
    
    FileHandler.write_to_json(paths, args.paths, logger)
    #python main.py -gen -p settings.json -k 16
    #python main.py -enc -p settings.json
    #python main.py -dec -p settings.json
    #python main.py -p settings.json -ch decrypted_text,classes\\files\\decrypted.txt