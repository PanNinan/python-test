#  线程

from random import randint
from threading import Thread
from time import time, sleep


def download(file_name):
    print('开始下载%s' % file_name)
    time_use = randint(5, 10)
    sleep(time_use)
    print('%s下载成功,耗时%d秒' % (file_name, time_use))


def main():
    start = time()
    t1 = Thread(target=download, args=('Python从入门到住院.pdf',))
    t1.start()
    t2 = Thread(target=download, args=('Peking Hot.avi',))
    t2.start()
    t1.join()
    t2.join()
    end = time()
    print('总管耗时%.2f秒' % (end - start))


if __name__ == '__main__':
    main()
