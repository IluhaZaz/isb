import argparse
from utils.alphabet import rus_alf as alf

def encode(input_file: str, output_file: str, shift: int):

    """
    Encoding text from input_file with cesar's chipher with alphabet rotated by 'shift' times
    """

    res: str = ""

    with open(input_file, mode = "r", encoding = "utf-8") as f:
        s: str = f.readlines()
        s = "".join(s)
        s = s.upper()

    encoded_alf: str = alf[shift:] + alf[:shift]

    encoded_dict = dict()

    for i, j in zip(encoded_alf, alf):
        encoded_dict[j] = i
    
    
    for i in s:
        res += encoded_dict.get(i, i)

    with open(output_file, mode = "w", encoding = "utf-8") as f:
        f.write(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Cesar's chipher encoder")
    parser.add_argument("input_file", type = str, help = "Input file name")
    parser.add_argument("output_file", type = str, help = "Output file name")
    parser.add_argument('shift', type = int, help = 'Nums for rotation of alf')

    args = parser.parse_args()

    encode(args.input_file, args.output_file, args.shift)
    #python task_1\\cesar_encoder.py task_1\\files\\input.txt task_1\\files\\output.txt 3