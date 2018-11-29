"""
For_4.2 Coursera Task
"""


class Value:
    def __init__(self):
        return

    def __get__(self, instance, owner):
        return self._val

    def __set__(self, instance, value):
        self._val = value * (1 - instance.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission




def _main():
    new_account = Account(0.5)
    new_account.amount = 99

    print(new_account.amount)



if __name__ == "__main__":
    _main()
