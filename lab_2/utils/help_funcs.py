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
