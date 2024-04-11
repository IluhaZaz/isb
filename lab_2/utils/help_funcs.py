from logging import Logger


def max_ones_seq(seq: str) -> int:
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


def read_file(file: str, logger: Logger) -> str:
    res = ""
    try:
        with open(file, mode = "r", encoding = "utf-8") as f:
            res = f.read()
    except:
        logger.critical("Can't open input file")
    return res