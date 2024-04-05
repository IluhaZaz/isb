import argparse
import logging

from collections import Counter

from utils.constants import ALPHABETS
from utils.io_to_file import *


def decode(input_file: str, output_file: str, key_file: str, shift: int = None):

    alf = ALPHABETS["rus_alf"]

    """
    Decoding text from input_file with cesar's chipher with alphabet rotated by 'shift' times
    """

    res: str = ""
    s = read_file(input_file, logger)
    s = s.upper()

    if not shift:
        c = Counter(s)

        shift: int = ord(c.most_common()[0][0]) - ord("О")

    encoded_alf: str = alf[shift:] + alf[:shift]

    decoded_dict = dict()

    for i, j in zip(encoded_alf, alf):
        decoded_dict[i] = j
    
    res: str = ""

    for i in s:
        res += decoded_dict.get(i, i)
        
    write_to_file(output_file, res, logger)

    write_to_json(decoded_dict, key_file, logger)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = decode.__doc__)
    parser.add_argument("input_file", type = str, help = "Input file name")
    parser.add_argument("output_file", type = str, help = "Output file name")
    parser.add_argument("key_file", type = str, help = "File name to save decoded key")
    parser.add_argument('--shift', type = int, default = None, help = 'Nums for rotation of alf')

    args = parser.parse_args()

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)

    logger = logging.getLogger(__name__)

    decode(args.input_file, args.output_file, args.key_file, args.shift)

    #python task_1\\cesar_decoder.py task_1\\files\\output.txt task_1\\files\\ex.txt task_1\\files\\key.json --shift 3