import argparse
import logging

from task_1.utils.constants import ALPHABETS
from utils.io_to_file import write_to_file, read_file


def encode(input_file: str, output_file: str, shift: int):

    alf = ALPHABETS["rus_alf"]

    """
    Encoding text from input_file with cesar's chipher with alphabet rotated by 'shift' times
    """

    res: str = ""

    s = read_file(input_file, logger)
    s = s.upper()

    encoded_alf: str = alf[shift:] + alf[:shift]

    encoded_dict = dict()

    for i, j in zip(encoded_alf, alf):
        encoded_dict[j] = i
    
    for i in s:
        res += encoded_dict.get(i, i)

    write_to_file(output_file, res, logger)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = encode.__doc__)
    parser.add_argument("input_file", type = str, help = "Input file name")
    parser.add_argument("output_file", type = str, help = "Output file name")
    parser.add_argument('shift', type = int, help = 'Nums for rotation of alf')

    args = parser.parse_args()

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)

    logger = logging.getLogger(__name__)

    encode(args.input_file, args.output_file, args.shift)
    #python task_1\\cesar_encoder.py task_1\\files\\input.txt task_1\\files\\output.txt 3