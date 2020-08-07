# encoding = utf-8
import random
import threading
import time
from queue import Queue

import redis
import requests
from bs4 import BeautifulSoup

# 连接池
conn_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', decode_responses=True)


# 获取小说所有章节分页html地址
def get_chapter_page_list(html, chapter_queue):
    print('章节URL采集线程开启...')
    target_html = get_page(html)
    soup = get_soup(target_html)
    try:
        page_select = soup.find_all(name="option")
        chapter_page = []
        for option in page_select:
            href = domain + option['value']
            chapter_page.append(href)
        for item in chapter_page:
            get_all_chapter(item, chapter_queue)
        print('章节URL采集线程结束...')
    except Exception as e:
        print('解析所有章节列表网址出错:' + str(e))


# 获取所有章节
def get_all_chapter(url, chapter_queue):
    chapter_html = get_page(url)
    soup = get_soup(chapter_html)
    uls = soup.find_all(name="ul")
    tag_a = uls[4].find_all(name="a")
    rs = redis.Redis(connection_pool=conn_pool)
    for item in tag_a:
        chapter_url = domain + item['href']
        # get_detail(chapter_url)
        print(chapter_url)
        chapter_queue.put(chapter_url)  # 每章节url放入队列


# 获取小说内容
def get_detail(chapter_queue):
    try:
        while chapter_queue.empty() is not True:
            html = chapter_queue.get(timeout=3)
            text = get_page(html)
            soup = get_soup(text)
            pb_next = soup.find(name="h1", id="chaptertitle").get_text(strip=True)
            max = pb_next[-3]
            rs = redis.Redis(connection_pool=conn_pool)
            if int(max) > 1:  # 有分页内容
                for i in range(int(max)):
                    i_html = html.replace(".html", "") + "_" + str(i + 1) + ".html"
                    content = get_content(i_html)
                    score = get_score_from_url(i_html)
                    rs.zadd('ebook', {content: score})
            else:
                content = get_content(html)
                score = get_score_from_url(html)
                rs.zadd('ebook', {content: score})
    except Exception as e:
        print('出错' + str(e))


# 获取页面html源码
def get_page(url):
    page = requests.get(url, headers=headers)
    byte_text = page.text.encode('utf-8')
    return str(byte_text, encoding="utf-8")


# 获取soup对象
def get_soup(html):
    return BeautifulSoup(html, 'lxml')


# 获取页面小说文本
def get_content(html):
    text = get_page(html)
    soup = get_soup(text)
    div = soup.find(name="div", class_="novelcontent")
    ps = div.find_all(name="p")
    # title = ps[0].get_text() + "\n"
    content = ps[1].get_text() + "\n"
    return content


def get_score_from_url(url):
    tail_str = url.split('/')[-1].split('.')[0]
    if tail_str.find('_') != -1:
        url_number = tail_str.split('_')
        return int(url_number[0]) + int(url_number[1])
    else:
        return int(tail_str)


domain = 'https://m.vcxsw.com/'
target_url = 'https://m.vcxsw.com/vc/100/100301/index_1.html'  # 目标采集网址
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.106 Safari/537.36 ',
    'Referrer': 'https://m.vcxsw.com'
}
txt_content = {}  # 存储小说所有内容
chapters = []

thread_list = []
if __name__ == '__main__':
    rs = redis.Redis(connection_pool=conn_pool)
    data = rs.zrange('ebook', 0, -1, desc=False, withscores=True)
    with open('xxx.txt', 'a', encoding="utf-8") as file:
        for item in data:
            file.write(item[0])
    file.close()
    exit()

    begin = time.time()
    spider_threads = []
    chapter_queue = Queue()
    T = threading.Thread(target=get_chapter_page_list, args=(target_url, chapter_queue,))
    T.start()
    T.join()
    for i in range(10):
        t = threading.Thread(target=get_detail, args=(chapter_queue,))
        spider_threads.append(t)
    for t in spider_threads:
        t.start()
    for t in spider_threads:
        t.join()
    print('\n子线程运行完毕')
    end = time.time()
    print('下载完毕，总耗时', end - begin, '秒')
    # with open('1.txt', 'a', encoding="utf-8") as file:
    # file.close()
    # begin = time.time()
    # chaptername = Queue()  # 存放小说章节地址
    # for id in range(11):
    #     thread1 = MyTread(id, str(id), id)
    #     thread_list.append(thread1)
    # for t in thread_list:
    #     t.setDaemon(False)
    #     t.start()
    # 
    # for t in thread_list:
    #     t.join()
    # print('\n子线程运行完毕')
    # txtcontent1 = sorted(txt_content)
    # file = codecs.open('page_url.txt', 'w', 'utf-8')  # 小说存放在本地的地址
    # chaptercount = len(chaptername)
    # 
    # # 写入文件中
    # for ch in range(chaptercount):
    #     title = '\n           第' + str(ch + 1) + '章  ' + str(chaptername[ch]) + '         \n\n'
    #     content = str(txt_content[txtcontent1[ch]])
    #     file.write(title + content)
    # file.close()
    # end = time.time()
    # print('下载完毕，总耗时', end - begin, '秒')
