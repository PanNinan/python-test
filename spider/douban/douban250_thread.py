import re
import threading
import time
from queue import Queue
from threading import Thread

import redis
import requests
from bs4 import BeautifulSoup


def run(in_q):
    headers = {
        'Referer': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    while in_q.empty() is not True:
        url = in_q.get()
        data = requests.get(url, headers=headers)
        r = data.content
        content = str(r, encoding='utf-8', errors='ignore')
        bs = BeautifulSoup(content, 'lxml')
        divs = bs.find_all(name="div", class_="item")
        for item in divs:
            data = []
            titles = item.find_all(name="span", class_="title")
            if 2 == len(titles):
                title_zh = titles[0].get_text(strip=True)
                title_en = titles[1].get_text(strip=True).replace("/", "")
            else:
                title_zh = titles[0].get_text(strip=True)
                title_en = ''
            data.append(title_zh)
            data.append(title_en)
            pic_href = item.find(name="img")['src']
            data.append(pic_href)
            info_url = item.find(name="a")['href']
            data.append(info_url)
            rating_num = item.find(name="span", class_="rating_num").get_text()
            data.append(rating_num)
            rate_person = item.select(".star span")[-1].get_text()
            rate_person_num = re.findall(r"\d+\.?\d*", rate_person)[0]
            data.append(rate_person_num)
            inq = item.find(name="span", class_="inq")
            if inq is not None:
                inq = inq.get_text(strip=True)
            else:
                inq = ''
            data.append(inq)
            summary = item.find(name="div", class_="bd").p.get_text(strip=True)
            data.append(summary)
            rds = redis.Redis(connection_pool=conn_pool)
            rds.set(title_zh, '|'.join(data))
            t = threading.currentThread()
            print('Thread id:{}-Thread name:{}-{}已存储'.format(t.ident, t.getName(), title_zh))
        in_q.task_done()


if __name__ == '__main__':
    start = time.time()
    queue = Queue()
    result_queue = Queue()
    conn_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', decode_responses=True)
    base_url = 'https://movie.douban.com/top250?start='
    for i in range(0, 10):
        url = base_url + str(i * 25)
        queue.put(url)
    print('queue 开始大小 %d' % queue.qsize())

    for index in range(5):
        thread = Thread(target=run, args=(queue,))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()

    queue.join()  # 队列消费完 线程结束
    end = time.time()
    print('总耗时：%s' % (end - start))
    print('queue 结束大小 %d' % queue.qsize())
    print('result_queue 结束大小 %d' % result_queue.qsize())
