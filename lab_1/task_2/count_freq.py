from collections import Counter

def decode(input_file: str, output_file: str):
    with open(input_file, mode = "r", encoding = "utf-8") as file:
        s = file.read()

    c = Counter(s)
    l = len(s)
    
    with open(output_file, mode = "w", encoding = "utf-8") as file:
        for key, val in c.most_common():
            file.write(f"{key}: {round(val/l, 5)}\n")

if __name__ == "__main__":
    decode("lab_1\\task_2\\files\\cod8.txt", "lab_1\\task_2\\files\\freq.txt")