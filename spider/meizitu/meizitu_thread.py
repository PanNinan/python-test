import os
import time
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout


def mkdir(path):  # 这个函数创建文件夹
    path = path.strip()
    is_exists = os.path.exists(os.path.join("D:/code/tmp", path))
    if not is_exists:
        print(u'新建文件夹：', path)
        os.makedirs(os.path.join("D:/code/tmp", path))
        # os.chdir(os.path.join("D:/code/tmp", path))  # 切换到目录
        return True
    else:
        return False


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
                  "Chrome/19.0.1055.1 Safari/535.24",
    'Referer': 'https://www.mzitu.com',
    'Connection': 'close'
}


def all_url(page_url, uqueue):
    html_1 = request(page_url)  # 调用request函数把套图地址传进去会返回给我们一个response
    # title
    title = BeautifulSoup(html_1.text, 'lxml').find(
        'h2', class_='main-title').get_text()
    # 我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
    path = str(title).replace("?", '_')
    mkdir(path)
    # 获取底部分页栏
    pagenavi = BeautifulSoup(html_1.text, 'lxml').find(
        'div', class_='pagenavi').find_all('a')
    # 最后一页的a标签
    last_a = pagenavi[-2]
    # 最后一页页码数
    last_num = last_a.find('span').text
    for page in range(1, int(last_num) + 1):
        page_url = page_url + '/' + str(page)
        uqueue.put(path + '#' + page_url)


def html(href):  # 这个函数是处理套图地址获得图片的页面地址
    html_2 = request(href)
    headers['referer'] = href
    max_span = BeautifulSoup(html_2.text, 'lxml').find(
        'div', class_='pagenavi').find_all('span')[-2].get_text()
    for page in range(1, int(max_span) + 1):
        page_url = href + '/' + str(page)
        img(page_url)  # 调用img函数


def img(in_q):  # 这个函数处理图片页面地址获得图片的实际地址
    while in_q.empty() is not True:
        url = in_q.get(timeout=3)
        data = url.split('#')
        img_html = request(data[1])
        if img_html is not None:
            img_url = BeautifulSoup(img_html.text, 'lxml').find(
                'div', class_='main-image').find('img')['src']
            save(img_url, data[0])
        in_q.task_done()


def save(img_url, path):  # 这个函数保存图片
    name = img_url[-9:-4]
    f = open(r'D:/code/tmp/' + path + '/' + name + '.jpg', 'ab')
    f.write(request(img_url).content)
    f.close()
    print("%s保存完成！" % name)


def request(request_url):
    try:
        content = requests.get(request_url, headers=headers, timeout=5)
        return content
    except (ConnectionError, ReadTimeout):
        print('Crawling Failed', request_url)
        return None


if __name__ == '__main__':
    url = 'https://www.mzitu.com/62939'
    start = time.time()
    queue = Queue()
    if not os.path.exists('D:/code/tmp/'):
        os.makedirs('D:/code/tmp/')
    # 抓取所有图片url
    thread_1 = Thread(target=all_url, args=(url, queue,))
    thread_1.daemon = True  # 随主线程退出而退出
    thread_1.start()
    time.sleep(1)
    for index in range(5):
        # 获取图片内容并保存
        thread = Thread(target=img, args=(queue,))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()

    queue.join()  # 队列消费完 线程结束
    end = time.time()
    print('总耗时：%s' % (end - start))
