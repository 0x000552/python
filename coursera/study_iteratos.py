"""
Iterator's functions invoke order
"""

# decorate text with escape sequences
rbt = "\033[91;5m"  # red blink
clt = "\033[0m"  # reset text decoration


class MyIterator:
    def __init__(self, f_val=0, l_val=5):
        if f_val > l_val:
            raise ValueError("Argument rule: f_val > l_val")
        print(f"{rbt}init invoked{clt}")
        self.f_val = f_val
        self.l_val = l_val

    def __iter__(self):
        print(f"{rbt}itter invoked{clt}")
        self.var = self.f_val
        return self

    def __next__(self):
        print(f"{rbt}next invoked{clt}")
        if self.var < self.l_val:
            self.var += 1
            return self.var - 1
        else:
            raise StopIteration


mi = MyIterator(1, 3)
for i in mi:
    print(i)
print("")
for i in mi:
    print(i)
