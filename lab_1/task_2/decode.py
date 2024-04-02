from files.key import key

def decode(input_file: str, output_file: str):
    with open(input_file, mode = "r", encoding = "utf-8") as file:
        s = file.read()
    res = ""
    for i in s:
        res += key.get(i, i)
    
    with open(output_file, mode = "w", encoding = "utf-8") as file:
        file.write(res)

if __name__ == "__main__":
    decode("lab_1\\task_2\\files\\cod8.txt", "lab_1\\task_2\\files\\output.txt")