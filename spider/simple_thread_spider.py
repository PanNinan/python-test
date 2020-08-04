import time
import requests
import threading
from lxml import etree
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread


def run(in_q, out_q):
    headers = {
        'Referer': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    while in_q.empty() is not True:
        data = requests.get(url=in_q.get(), headers=headers)
        r = data.content
        content = str(r, encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html5lib')
        fixed_html = soup.prettify()
        html = etree.HTML(fixed_html)
        num = html.xpath('//span[@class="rating_num"]//text()')
        out_q.put(str(threading.current_thread().getName()) + '-' + str(num))
        in_q.task_done()


if __name__ == '__main__':
    start = time.time()
    queue = Queue()
    result_queue = Queue()
    for i in range(1, 26):
        queue.put('https://movie.douban.com/top250?start=' + str(i * 10))
    print('queue 开始大小 %d' % queue.qsize())

    for index in range(5):
        thread = Thread(target=run, args=(queue, result_queue,))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()

    queue.join()  # 队列消费完 线程结束
    end = time.time()
    print('总耗时：%s' % (end - start))
    print('queue 结束大小 %d' % queue.qsize())
    print('result_queue 结束大小 %d' % result_queue.qsize())
