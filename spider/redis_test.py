import time
from queue import Queue
import threading
import redis
from threading import Thread

# decode_responses为True取出内容自动decode
# 连接池
conn_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', decode_responses=True)
rs1 = redis.Redis(connection_pool=conn_pool)


def run(in_q):
    while in_q.empty() is not True:
        url = in_q.get()
        rs = redis.Redis(connection_pool=conn_pool)
        rs.sadd('url', url)
        in_q.task_done()


if __name__ == '__main__':
    start = time.time()
    queue = Queue()
    for i in range(1, 101):
        queue.put('https://movie.douban.com/top250?start=' + str(i))
    print('queue 开始大小 %d' % queue.qsize())

    for index in range(5):
        thread = Thread(target=run, args=(queue,))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
        thread.join()

    queue.join()  # 队列消费完 线程结束
    end = time.time()
    print('总耗时：%s' % (end - start))
    print('queue 结束大小 %d' % queue.qsize())
