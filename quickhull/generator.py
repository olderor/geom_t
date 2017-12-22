from random import randint
import os

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def gen_size(size):
    for t in range(100):
        path = "tests/" + str(size) + "/" + str(t) + ".txt"
        ensure_dir(path)
        f = open(path, 'w')
        f.writelines(str(size) + '\n')
        for i in range(size):
            f.writelines(str(randint(-100000, 100000)) + '\n')
        f.close()


gen_size(3)
gen_size(10)
gen_size(100)
gen_size(1000)
gen_size(100000)
gen_size(10000000)
