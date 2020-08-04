# 斐波那切数列生成器


def fib(n):
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
        yield a


if __name__ == '__main__':
    num = input('请输入个数n: ')
    for item in fib(int(num)):
        print(str(item).center(100, '*'))
