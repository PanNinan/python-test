from time import time


def main():
    total = 0
    number_list = range(1, 100000001)
    start = time()
    for i in number_list:
        total += i
    end = time()
    print('结果: %.2f' % total)
    print('计算完成,耗时%.2f秒' % (end - start))


if __name__ == '__main__':
    main()
