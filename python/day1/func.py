# map


def jia(value):
    return value + 1


def pf(value):
    return value ** 2


def test_func(array, func):
    if type(array) is not list:
        return False
    if not callable(func):
        return False
    res = []
    for item in array:
        re = func(item)
        res.append(re)
    return res


if __name__ == '__main__':
    test_list = [1, 2, 3, 4, 5, 6]

    result = test_func(test_list, pf)

    print(result)

    map_result = map(jia, test_list)

    print(list(map_result))

    res1 = map(lambda n: n > 5, range(10))
    lt1 = list(res1)
    print(lt1)

    res2 = filter(lambda n: n > 5, range(10))
    lt = list(res2)
    print(lt)
