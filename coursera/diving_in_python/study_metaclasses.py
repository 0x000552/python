from abc import ABCMeta, abstractmethod


print("Let's try metaclass:\n\n")
class MyMetaClass(type):
    """
    Metaclass which change all list fields in tuple
    """

    def __new__(mcls, clsname, bases, dict):
        print("In MyMetaClass.__new__()")
        for key, val in dict.items():
            if isinstance(val, list):
                dict[key] = tuple(val)

        return super().__new__(mcls, clsname, bases, dict)


class TestClass(metaclass=MyMetaClass):
    print("In TestClass")
    list_ = [1, 2, 3]
    tuple_ = [4, 5, 6]
    def __new__(cls, *args, **kwargs):
        print("in TestClass.__new__()")
        return super().__new__(cls, *args, **kwargs)

TestClass()
print(f"\nTestClass: list_ {TestClass.list_.__class__}._class_ == {TestClass.list_}")



print("\n\n\nNow test abstract class:\n")

class MyAbstractClass(metaclass=ABCMeta):
    def f0(self):
        print("f0 in MyAbstractClass")

    @abstractmethod
    def f1(self):
        print("f1 in MyAbstractClass")
    # raise NotImplementedError("Please Implement this method")  # Old

class AbstractImpl(MyAbstractClass):
    #def f0(self):
     #   print("f0 in AbstractImpl")

    def f1(self):  # if no f1 implementation - TypeError
        print("f1 in AbstractImpl")


impl = AbstractImpl()
impl.f0()
impl.f1()
# MyAbstractClass().f0()   # TypeError
