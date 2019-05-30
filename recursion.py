def func(n):
    if n < 10:
        n += 1
        return func(n)
    else:
        return n


if __name__ == '__main__':
    res = func(0)
    print(res)

    func1 = lambda x: x ** 2
    res = func1(2)

    print(res)
