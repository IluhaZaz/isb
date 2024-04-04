import json
import argparse
import logging


def decode(input_file: str, output_file: str, key_file: str):

    """
    Decoding text from input file with given key
    """

    try:
        with open(key_file, mode = "r", encoding = "utf-8") as file:
            key: dict = json.loads(file.read())
    except:
        logger.critical("Can't open key file")
        key = {}

    try:
        with open(input_file, mode = "r", encoding = "utf-8") as file:
            s = file.read()
    except:
        logger.critical("Can't open input file")
        s = ""
        
    res: str = ""
    for i in s:
        res += key.get(i, i)
    
    with open(output_file, mode = "w", encoding = "utf-8") as file:
        file.write(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = decode.__doc__)
    parser.add_argument("input_file", type = str, help = "Input file name")
    parser.add_argument("output_file", type = str, help = "Output file name")
    parser.add_argument("key_file", type = str, help = "File with key to decode")

    args = parser.parse_args()

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)

    logger = logging.getLogger(__name__)

    decode(args.input_file, args.output_file, args.key_file)
    #python task_2\\decode.py task_2\\files\\cod8.txt task_2\\files\\output.txt task_2\\files\\key.json