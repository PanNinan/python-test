import os
import time

import requests
from bs4 import BeautifulSoup

domain = 'https://www.diyibanzhu8.in/'
base_path = os.getcwd()
self_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.106 Safari/537.36",
}


def main(baseurl):
    url_list = parse_page(baseurl)  # 当前页面所有页面url列表
    save_from_list(url_list)
    next_url = get_next_url(baseurl)
    if next_url == baseurl:
        return
    else:
        main(next_url)
    return


def get_html(url, encode="gbk"):
    response = requests.get(url, headers=self_header)
    response.encoding = encode
    return response.text


def parse_page(url):
    html = get_html(url)
    bs = BeautifulSoup(html, "lxml")
    li_list = bs.find_all(name="ul", class_="list")[1]
    a_list = li_list.find_all(name="a")
    href_list = []
    for a in a_list:
        href_list.append(domain + a['href'])
    return href_list


def get_next_url(current_url):
    html = get_html(current_url)
    bs = BeautifulSoup(html, "lxml")
    next_href = bs.find(name="a", class_="nextPage")['href']
    return domain + next_href


def get_word(url):
    html = get_html(url)
    bs = BeautifulSoup(html, "lxml")
    div = bs.find_all(name="div", class_="page-content font-large")
    return div[0].p.get_text().replace(u'\xa0', u' ')


def save_from_list(url_list):
    with open(base_path + r'/tmp/鱼龙舞.txt', 'a') as file:
        for url in url_list:
            response = requests.get(url, headers=self_header)
            response.encoding = "gbk"
            html = response.text
            bs = BeautifulSoup(html, "lxml")
            div = bs.find_all(name="div", class_="page-content font-large")
            if bs.center is None:  # 页内无分页
                text = div[0].p.text
                file.write(text.replace(u'\xa0', u' ') + "\r")  # 替换中文的空格
                print('页面：' + url + '内容写入成功！')
            else:
                pages = bs.center
                pages = pages.find_all(name="a")
                for page in pages:
                    inner_url = baseurl + page['href']
                    text = get_word(inner_url)
                    file.write(text + "\r")
                    print('页面：' + inner_url + '内容写入成功！')
    file.close()
    return


if __name__ == '__main__':
    baseurl = 'https://www.diyibanzhu9.in/10/10793/'
    start = time.time()
    main(baseurl)
    end = time.time()
    print('采集完成，总耗时：%s' % (end - start))
