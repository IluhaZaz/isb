import argparse
import logging
import os
import sys

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from io_to_file import read_json, read_file, write_to_file


def decode(input_file: str, output_file: str, key_file: str):

    """
    Decoding text from input file with given key
    """

    key = read_json(key_file, logger)

    s = read_file(input_file, logger)
        
    res: str = ""
    for i in s:
        res += key.get(i, i)
    
    write_to_file(output_file, res, logger)


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