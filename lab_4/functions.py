import multiprocessing
import hashlib
import logging
import time
import matplotlib.pyplot as plt

from tqdm import tqdm

from io_to_file import FileHandler


def get_valide_card_num(hash: str, last_4_nums: str, bin: str) -> list[int]:

    res = []
    for middle_num in range(0, 999999 + 1):
        card_num: str = bin + str(middle_num).zfill(6) + last_4_nums
        if hashlib.sha3_256(card_num.encode()).hexdigest() == hash:
            res.append(card_num)
    return res


def find_number(hash: str, last_4_nums: str, bins: list[int], 
                path_to_save: str, logger: logging.Logger) -> list[int]:

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


def get_stats(hash: str, last_4_nums: str, bins: list[int], 
             logger: logging.Logger, path_to_save: str) -> list[float]:

    times = []
    
    for i in tqdm(range(1, int(1.5 * multiprocessing.cpu_count()) + 1), desc='Num of processes'):

        start = time.time()
        args = [(hash, last_4_nums, str(bin)) for bin in bins]
        with multiprocessing.Pool(i) as pool:
            pool.starmap(get_valide_card_num, args)
            times.append(time.time() - start)

    times = list(map(str, times))

    FileHandler.write_to_file(path_to_save, " ".join(times), logger)
    return times


def draw_graph(data: list[float], logger: logging.Logger, path_to_save: str):

    plt.plot(range(1, len(data) + 1), data)

    m = min(data)
    m = data.index(m)
    plt.scatter([m + 1], [data[m]], c = "red", )
    plt.annotate(f"Minimum point ({m + 1}, {round(data[m], 2)})", (m + 1, data[m]))

    plt.xlabel('Num of processes')
    plt.ylabel('Executable time, s')

    try:
        plt.savefig(path_to_save)
    except:
        logger.error("Graph didn't saved")

    plt.show()
