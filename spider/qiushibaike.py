# coding:utf-8

import threading
from queue import Queue

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.116 Safari/537.36 ",
    "referer": "https://www.qiushibaike.com/text/"
}


class CrawlThread(threading.Thread):
    def __init__(self, thread_id, _queue, _queue2):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = _queue
        self.queue2 = _queue2

    def run(self):
        print('线程{}启动'.format(self.thread_id))
        self.crawl_spider()
        print('线程{}退出'.format(self.thread_id))

    def crawl_spider(self):
        while True:
            if self.queue.empty():
                break
            else:
                page = self.queue.get()
                print('当前工作线程为{},正在采集第{}个页面'.format(self.thread_id, str(page)))
                url = 'https://www.qiushibaike.com/text/page/{}'.format(str(page))
                try:
                    response = requests.get(url, headers=headers)
                    byte_text = response.text.encode('utf-8')
                    self.queue2.put(str(byte_text, encoding="utf-8", errors='ignore'))
                except Exception as e:
                    print('something error', e)


class ParserThread(threading.Thread):

    def __init__(self, thread_id, _queue, file):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = _queue
        self.file = file

    def run(self):
        print('线程{}启动'.format(self.thread_id))
        while not flag:
            try:
                item = self.queue.get(False)
                if not item:
                    pass
                self.parse_data(item)
                self.queue.task_done()
            except Exception as e:
                print(e)
        print('线程{}退出'.format(self.thread_id))

    def parse_data(self, content):
        try:
            soup = BeautifulSoup(content, 'lxml')
            divs = soup.find_all(name="div", attrs={'class': ['typs_long', 'typs_hot']})
            for div in divs:
                # author = div.h2.get_text()
                # img_url = div.img['src']
                content = div.span.get_text(strip=True)
                self.file.write(content + "\n")
        except Exception as e:
            print(e)
        return


flag = False


def main():
    data_queue = Queue()
    output = open('../tmp/qiushi.txt', 'a', encoding='utf-8')
    page_queue = Queue(50)
    for page in range(1, 31):
        page_queue.put(page)

    # 初始化采集线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, page_queue, data_queue)
        thread.start()
        crawl_threads.append(thread)

    # 初始化解析线程
    parser_threads = []
    parser_name_list = ['parser_1', 'parser_2', 'parser_3']
    for thread_id in parser_name_list:
        thread = ParserThread(thread_id, data_queue, output)
        thread.start()
        parser_threads.append(thread)

    while not page_queue.empty():
        pass

    for thread in crawl_threads:
        thread.join()

    while not data_queue.empty():
        pass

    global flag
    flag = True

    for thread in parser_threads:
        thread.join()

    output.close()


if __name__ == '__main__':
    main()
