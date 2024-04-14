import logging
import argparse
import math

from scipy.special import gammainc

from constants import pi


#Part with help funcs
def max_ones_seq(seq: str) -> int:

    """
    Counts max length of ones sequence in 'seq'
    """

    res = 0
    c = 0
    for i in seq:
        if i == "1":
            c += 1
        else:
            res = max(res, c)
            c = 0
    res = max(res, c)
    return res


def read_file(file: str, logger: logging.Logger) -> str:

    """
    Reads data from 'file'
    """

    res = ""
    try:
        with open(file, mode = "r", encoding = "utf-8") as f:
            res = f.read()
    except:
        logger.critical("Can't open input file")
    return res


def error_handler(func, logger: logging.Logger):

    """
    Catches errors that may occure during 'func' execution
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.critical("Error encountered")
    return wrapper


#Main funcs for tests
def frequency_bit_test(seq: str) -> float:

    """
    Performs frequency bit test and returns
    P, which is probability that seq is random
    """

    sn = abs(sum([1 if i == "1" else -1 for i in seq]))/math.sqrt(len(seq))
    return math.erfc(sn/math.sqrt(2))


def same_consecutive_bits(seq: str) -> float:

    """
    Performs same consecutive bits test and returns
    P, which is probability that seq is random
    """

    n: int = len(seq)
    ones_part: float = seq.count("1")/n

    if abs(ones_part - 0.5) >= 2/math.sqrt(n):
        return 0
    
    vn: int = sum([0 if seq[i] == seq[i + 1] else 1 for i in range(n - 1)])

    return math.erfc(abs(vn - 2 * n * ones_part * (1 - ones_part))/(2*math.sqrt(2 * n) * ones_part * (1 - ones_part)))


def longest_ones_seq(seq: str) -> float:

    """
    Permorms longest ones sequence test and returns
    P, which is probability that seq is random
    """

    n = len(seq)
    blocks: int = n//8

    seq_lens = []

    for i in range(blocks):
        seq_lens.append(max_ones_seq(seq[i*8: i*8 + 8]))
    
    v1 = seq_lens.count(0) +  seq_lens.count(1)
    v2 = seq_lens.count(2)
    v3 = seq_lens.count(3)
    v4 = blocks - v1 - v2 - v3
    v = [v1, v2, v3, v4]

    xi2 = sum([math.pow(v[i] - 16 * pi[i], 2)/(16 * pi[i]) for i in range(4)])

    return gammainc(1.5, xi2/2)


def main(cpp_seq: str, java_seq: str) -> None:

    print(f"'P' value for frequency bit test(C++): {frequency_bit_test(cpp_seq)}")
    print(f"'P' value for frequency bit test(Java): {frequency_bit_test(java_seq)}")

    print(f"'P' value for same consecutive bits test(C++): {same_consecutive_bits(cpp_seq)}")
    print(f"'P' value for same consecutive bits test(Java): {same_consecutive_bits(java_seq)}")

    print(f"'P' value for longest ones sequences test(C++): {longest_ones_seq(cpp_seq)}")
    print(f"'P' value for longest ones sequences test(Java): {longest_ones_seq(java_seq)}")


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

    frequency_bit_test = error_handler(frequency_bit_test, logger)
    same_consecutive_bits = error_handler(same_consecutive_bits, logger)
    longest_ones_seq = error_handler(longest_ones_seq, logger)

    main(cpp_seq, java_seq)
    #python nist_tests.py random_generators\\files\\cpp_gen.txt random_generators\\files\\java_gen.txt