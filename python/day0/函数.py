# 函数

from module_1 import foo as f1
from module_2 import foo as f2


def add(*args):
    result = 0
    for item in args:
        result += int(item)
    return result


result = add(1, 2, 3, 4)
print(result)
f1()
f2()


def foo():
    b = 'hello'

    def bar():  # Python中可以在函数内部再定义函数
        c = True
        print(a)
        print(b)
        print(c)

    bar()
    # print(c)  # NameError: name 'c' is not defined


if __name__ == '__main__':
    a = 100
    # print(b)  # NameError: name 'b' is not defined
    foo()
