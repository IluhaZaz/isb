import multiprocessing
import hashlib
import logging

from io_to_file import FileHandler


def get_valide_card_num(hash: str, last_4_nums: str, bin: str) -> list[int]:

    res = []
    for middle_num in range(0, 999999 + 1):
        card_num: str = bin + str(middle_num).zfill(6) + last_4_nums
        if hashlib.sha3_256(card_num.encode()).hexdigest() == hash:
            res.append(card_num)
    return res


def find_number(hash: str, last_4_nums: str, bins: list[int], path_to_save: str, logger: logging.Logger) -> list[int]:

    ans = []
    args = [(hash, last_4_nums, str(bin)) for bin in bins]
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for res in pool.starmap(get_valide_card_num, args):
            ans += res

    FileHandler.write_to_file(path_to_save, "\n".join(ans), logger)
    return ans


def help_sum(num: int) -> int:

    res = 0

    while num:
        res += num % 10
        num //= 10
    return res


def luhn_algorithm(card_number: str) -> bool:
    
    temp = card_number[::-1][1:]
    s: int = 0

    for i in range(len(temp)):
        if(i%2 == 0):
            s += help_sum(int(temp[i])*2)
        else:
            s += int(temp[i])
    
    c: int = 10 - ((s % 10) % 10)

    return c == int(card_number[-1])
    
