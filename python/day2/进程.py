# 进程

from multiprocessing import Process
from os import getpid
from random import randint
from time import time, sleep


def download_task(file_name):
    print('启动下载进程,进程号[%d]' % getpid())
    print('开始下载%s...' % file_name)
    time_use = randint(5, 10)
    sleep(time_use)
    print('%s下载结束,耗时%d秒' % (file_name, time_use))


def main():
    start = time()
    p1 = Process(target=download_task, args=('Python从入门到住院.pdf',))
    p1.start()
    p2 = Process(target=download_task, args=('TokyoHot.avi',))
    p2.start()
    p1.join()
    p2.join()
    end = time()
    print('总管耗时%.2f秒' % (end - start))


if __name__ == '__main__':
    main()
