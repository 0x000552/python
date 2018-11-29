"""
For 4.1 Coursera Task
"""
import tempfile
import os


class File:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        # self.read_stream = open(self.path, "r")
        with open(self.path, "r") as f:
            yield from f
        # return self

    def __next__(self):
        pass
        # return self.read_stream.readline()


    def __add__(l_addend, r_addend):
        new_file_name = f"{os.path.basename(l_addend.path)}_and_{os.path.basename(r_addend.path)}"
        new_file_path = os.path.join(tempfile.gettempdir(), new_file_name)

        # OMG... I believe it's not big
        with open(new_file_path, "w") as new_file:
            with open(l_addend.path, "r") as l_file:
                new_file.write(l_file.read())
            with open(r_addend.path, "r") as r_file:
                new_file.write(r_file.read())

        return type(l_addend)(new_file_path)

    def __str__(self):
        return self.path

    def write(self, str):
        with open(self.path, "a") as f:
            f.write(str)

if __name__ == "__main__":
    first = File('first.log')
    second = File('second.log')

    first.write('line\n')
    first.write('line\n')
    second.write('43g\n')

    new_obj = first + second

    print(new_obj)
    for line in new_obj:
        print(line.encode())
