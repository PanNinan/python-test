# 装饰器

import time


def timer(fun):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = fun(*args, **kwargs)
        stop_time = time.time()
        print('程序运行%s秒' % (stop_time - start_time))
        return res

    return wrapper


@timer
def test(name='TT', age=18):
    time.sleep(0.3)
    return '你好%d岁的%s' % (age, name)


print(test('ninan', 19))
