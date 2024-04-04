import argparse

from collections import Counter

def count_freq(input_file: str, output_file: str):

    """
    Count frequency for each letter in input file
    """

    with open(input_file, mode = "r", encoding = "utf-8") as file:
        s = file.read()

    c = Counter(s)
    l = len(s)
    
    with open(output_file, mode = "w", encoding = "utf-8") as file:
        for key, val in c.most_common():
            file.write(f"{key}: {round(val/l, 5)}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = count_freq.__doc__)
    parser.add_argument("input_file", type = str, help = "Input file name")
    parser.add_argument("output_file", type = str, help = "Output file name")

    args = parser.parse_args()
    count_freq(args.input_file, args.output_file)
    #python task_2\\count_freq.py task_2\\files\\cod8.txt task_2\\files\\freq.txt