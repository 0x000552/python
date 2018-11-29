"""
OOP is amazing...
"""

"""
class A(object):
    def __init__(self):
        print(f"{id(self)}\nA and mro for self: {type(self).__mro__}")
        super().__init__()


class B(object):
    def __init__(self):
        print("B")
        super().__init__()


class C(A, B):
    def __init__(self):
        print(id(self))
        A.__init__(self)
        B.__init__(self)


[x.__name__ for x in C.__mro__]
print("Calls:")
C()
"""

"""
class A:
    def __init__(self):
        self._var = 0

    @property
    def var(self):
         print("Getting var")
         return self._var
    print(id(var))
    @var.setter
    def var(self, value):
        print("Setting var")

class B(A):
    var = 2


a = A()
a.var
"""
from random import randint as ri


class ItemHolder:
    def __init__(self, _list=[]):
        if not isinstance(_list, list):  # TODO should I use type() insted
            raise TypeError("Argument should be type list")
        self._list = _list or [ri(1, 1552566551) * (12 ** ri(1, 10)) for _ in range(1001)]
        self.item_max = 0
        self.ph_index = 0
        self.ph_value = 0
        self.placeholder_init()

    def placeholder_init(self, new=0):
        self.ph_index = len(str(len(self._list)))
        if new:
            if abs(new) > abs(self.item_max):
                self.item_max = new
            else:
                return
        else:
            self.item_max = max(self._list)
            item_min = min(self._list)
            if self.item_max < abs(item_min):
                self.item_max = item_min
        self.ph_value = len(str(self.item_max))

    def __getitem__(self, index):
        return self._list[index]

    def __repr__(self):
        last_item_index = len(self._list) - 1
        str_list = ["[\n"]
        for index, value in enumerate(self._list):
            str_list.append(f"    item[{index: >{self.ph_index}}] == {value:>{self.ph_value}}")
            str_list.append("\n" if last_item_index == index else ",\n")
        str_list.append("]")
        return "".join(str_list)

    def __str__(self):
        print("STTTTR!!!")
        str_list = [f"[{index: >{self.ph_index}}] == {value:.>{self.ph_value}}" for index, value in
                    enumerate(self._list)]
        return "\n".join(str_list)

    def __setitem__(self, index, value):
        prev = self._list[index]  # or "None"
        self._list[index] = value
        self.placeholder_init(value)
        print(f"[{index: >{self.ph_index}}] =  {value:.>{self.ph_value}}, prev: {prev}\n")


items = ItemHolder()

items[6] = -75297267278278278278288888888
print(f"__str__:\n{items}:s\n\n")
print(f"__repr__:\n{items!r}")




print("\n\nLet's try power of descriptors...")
class myDesc:
    def __init__(self):
        print("init")
    def __get__(self, obj, type=None):
        print("get")
        return self
    def __call__(self, *args, **kwargs):
        print("call")

class foo:
    var = myDesc()


foo.var()