import logging
import argparse
import os
import sys
import math

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from io_to_file import read_file


def frequency_bit_test(seq: str) -> float:
    sn = abs(sum([1 if i == "1" else -1 for i in seq]))/math.sqrt(len(seq))
    return math.erfc(sn/math.sqrt(2))


def main(cpp_seq: str, java_seq: str, logger: logging.Logger):
    print(f"'P' value for frequency bit test(C++): {frequency_bit_test(cpp_seq)}")
    print(f"'P' value for frequency bit test(Java): {frequency_bit_test(java_seq)}")


if __name__ == "__main__":

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
    )
    
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()

    parser.add_argument("cpp_seq_file", type = str, help = "File with cpp random bit sequence")
    parser.add_argument("java_seq_file", type = str, help = "File with java random bit sequence")

    args = parser.parse_args()

    cpp_seq: str = read_file(args.cpp_seq_file, logger)
    java_seq: str = read_file(args.java_seq_file, logger)

    main(cpp_seq, java_seq, logger)
    #python tests\\nist_tests.py random_generators\\files\\cpp_gen.txt random_generators\\files\\java_gen.txt