# -*- coding:UTF-8 -*-
import collections
import re
import threading
import time
from queue import Queue
from urllib import request

import redis
from bs4 import BeautifulSoup

# 连接池
conn_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', decode_responses=True)

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, '
                  'like Gecko) Chrome/18.0.1025.166  Safari/535.19', }


def get_download_url(target_url):
    charter = re.compile(u'[第弟](.+)章', re.IGNORECASE)
    target_req = request.Request(url=target_url, headers=header)
    target_response = request.urlopen(target_req)
    target_html = target_response.read().decode('gbk', 'ignore')
    listmain_soup = BeautifulSoup(target_html, 'lxml')
    chapters = listmain_soup.find_all('div', class_='listmain')
    download_soup = BeautifulSoup(str(chapters), 'lxml')
    novel_name = str(download_soup.dl.dt).split("》")[0][5:]
    flag_name = "《" + novel_name + "》" + "正文卷"
    # number = (len(download_soup.dl.contents) - 1) / 2 - 8
    download_dict = collections.OrderedDict()
    begin_flag = False
    number = 1
    for child in download_soup.dl.children:
        if child != '\n':
            if child.string == u"%s" % flag_name:
                begin_flag = True
            if begin_flag is True and child.a is not None:
                download_url = "https://www.biqukan.com" + child.a.get('href')
                download_name = child.string
                if str(download_name).find('章') != -1:
                    names = str(download_name).split('章')
                    name = charter.findall(names[0] + '章')
                else:
                    names = ['', str(download_name)]
                    name = str(download_name)
                if name:
                    download_dict['第' + str(number) + '章 ' + names[1]] = download_url
                    number += 1
    return novel_name + '.txt', number, download_dict


def downloader(queue):
    print('%s启动' % threading.currentThread().getName())
    while queue.empty() is not True:
        print(queue.qsize())
        url = queue.get()
        download_req = request.Request(url=url, headers=header)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('gbk', 'ignore')
        soup_texts = BeautifulSoup(download_html, 'lxml')
        texts = soup_texts.find_all(id='content', class_='showtxt')
        soup_text = BeautifulSoup(str(texts), 'lxml').div.text.replace('\xa0', '')
        score = url.split('/')[-1].replace('.html', '')
        print(score)
        rds = redis.Redis(connection_pool=conn_pool)
        rds.zadd('ebook', {soup_text: score})
    print('%s退出' % threading.currentThread().getName())


if __name__ == "__main__":
    # print("\n\t\t欢迎使用《笔趣看》小说下载小工具\n\n\t\t\n")
    # print("*************************************************************************")
    # 小说地址
    # target_url = str(input("请输入小说目录下载地址:\n"))
    begin = time.time()
    target_url = 'https://www.biqukan.com/2_2760/'
    name, numbers, url_dict = get_download_url(target_url)
    queue = Queue()
    for key, value in url_dict.items():
        queue.put(value)
    print('队列写入完毕，开始抓取')
    spider_threads = []
    for i in range(25):
        t = threading.Thread(target=downloader, args=(queue,))
        spider_threads.append(t)
    for t in spider_threads:
        t.start()
    for t in spider_threads:
        t.join()
    print('抓取结束，开始写入文件')
    rs = redis.Redis(connection_pool=conn_pool)
    data = rs.zrange('ebook', 0, -1, desc=False, withscores=True)
    with open(name + '.txt', 'a', encoding="utf-8") as file:
        for item in data:
            file.write(item[0])
    file.close()
    end = time.time()
    print('下载完毕，总耗时', end - begin, '秒')
