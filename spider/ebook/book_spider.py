# encoding = utf-8
from queue import Queue

import requests
from bs4 import BeautifulSoup


# 获取小说所有章节分页html地址
def get_chapter_page_list(html):
    target_html = get_page(html)
    soup = get_soup(target_html)
    try:
        page_select = soup.find_all(name="option")
        for option in page_select:
            href = domain + option['value']
            chapter_page.append(href)
            # chapter_page_queue.put(href)
        return chapter_page
    except Exception as e:
        print('解析所有章节列表网址出错:' + str(e))


# 获取所有章节
def get_all_chapter(url):
    with open('q.txt', 'w') as file:
        chapter_html = get_page(url)
        soup = get_soup(chapter_html)
        uls = soup.find_all(name="ul")
        tag_a = uls[4].find_all(name="a")
        for item in tag_a:
            chapter_url = domain + item['href']
            # chapter_queue.put(chapter_url)
            file.write(chapter_url + "\n")
    file.close()


# 获取章节内容
def get_detail(html):
    try:
        text = get_page(html)
        soup = get_soup(text)
        pb_next = soup.find(name="h1", id="chaptertitle").get_text(strip=True)
        max = pb_next[-3]
        if int(max) > 1:  # 有分页内容
            for i in range(int(max)):
                i_html = html.replace(".html", "") + "_" + str(i + 1) + ".html"
                content = get_content(i_html)
        else:
            content = get_content(html)
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
    title = ps[0].get_text() + "\n"
    content = ps[1].get_text() + "\n"
    # print(title, content)
    # exit()


domain = 'https://m.vcxsw.com/'
target_url = 'https://m.vcxsw.com/vc/100/100301/index_1.html'  # 目标采集网址
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.106 Safari/537.36 ',
    'Referrer': 'https://m.vcxsw.com'
}
txt_content = {}  # 存储小说所有内容
chapter_page_queue = Queue()
chapter_queue = Queue()
chapter_page = []
chapters = []

thread_list = []
if __name__ == '__main__':
    accept_chapters = get_chapter_page_list(target_url)
    for item in accept_chapters:
        get_all_chapter(item)
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
    # file = codecs.open('q.txt', 'w', 'utf-8')  # 小说存放在本地的地址
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
