import multiprocessing
import hashlib
import logging

from io_to_file import FileHandler


def valide_card_num(hash: str, last_4_nums: str, bin: str):

    res = []
    for middle_num in range(0, 999999 + 1):
        card_num: str = str(bin) + str(middle_num).zfill(6) + last_4_nums
        if hashlib.sha3_256(card_num.encode()).hexdigest() == hash:
            res.append(card_num)
    return res


def find_number(hash: str, last_4_nums: str, bins: list[int], path_to_save: str, logger: logging.Logger):

    ans = []
    args = [(hash, last_4_nums, str(bin)) for bin in bins]
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for res in pool.starmap(valide_card_num, args):
            ans += res

    FileHandler.write_to_file(path_to_save, "\n".join(ans), logger)
    return ans


def luna_algorithm():
    pass
