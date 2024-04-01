from collections import Counter

from utils.alphabet import rus_alf as alf


def decode(input_file, output_file, shift: int = None):

    res = ""

    with open(input_file, mode = "r", encoding = "utf-8") as f:
        s: str = f.read()
        s = s.upper()

    if not shift:
        c = Counter(s)

        shift: int = ord(c.most_common()[0][0]) - ord("О")

    encoded_alf: str = alf[shift:] + alf[:shift]

    decoded_dict = dict()

    for i, j in zip(encoded_alf, alf):
        decoded_dict[i] = j
    
    res = ""

    for i in s:
        res += decoded_dict.get(i, i)
    with open(output_file, mode = "w", encoding = "utf-8") as f:
        f.write(res)


if __name__ == "__main__":
    decode("lab_1\\task_1\\files\\output.txt", "lab_1\\task_1\\files\\ex.txt", 3)