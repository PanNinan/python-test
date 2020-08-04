# -*- coding:utf-8 -*-

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import bs4
import os


class Pic():
    def __init__(self, url, range):
        self.url = url
        if not self.url:
            self.url = 'https://www.buxiuse.com/?'
        self.range = range

    def get_html(self, url, header=None):
        """请求初始url"""
        requests.packages.urllib3.disable_warnings()  # 屏蔽warning报错
        response = requests.get(url, headers=header, verify=False)
        try:
            if response.status_code == 200:
                # print(response.status_code)
                # print(response.text)
                return response.text
            return None
        except RequestException:
            print("请求失败")
            return None

    def parse_html(self, html, list_data):
        """提取img的名称和图片url，并将名称和图片地址以字典形式返回"""
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find_all('img')
        for t in img:
            if isinstance(t, bs4.element.Tag):
                # print(t)
                name = t.get('alt')
                img_src = t.get('src')
                list_data.append([name, img_src])
        dict_data = dict(list_data)
        return dict_data

    def get_image_content(self, url):
        """请求图片url，返回二进制内容"""
        print("downloading", url)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.content
            return None
        except RequestException:
            return None

    def download(self):
        base_url = self.url
        for i in range(1, self.range):
            url = base_url + 'cid=2&' + 'page=' + str(i)
            # print(url)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9, image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip,deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'www.dbmeinv.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/70.0.3538.102Safari/537.36'
            }
            list_data = []
            html = self.get_html(url)
            # print(html)
            dictdata = self.parse_html(html, list_data)

            root_dir = 'D:'
            tt = '大杂烩'
            if not os.path.exists(root_dir + '/pics'):
                os.makedirs(root_dir + '/pics')
            if not os.path.exists(root_dir + '/pics/' + str(tt)):
                os.makedirs(root_dir + '/pics/' + str(tt))

            save_path = root_dir + '/pics/' + '大杂烩'
            for t in dictdata.items():
                try:
                    file_path = save_path + '/' + t[0] + 'q' + '.jpg'
                    if not os.path.exists(file_path):  # 判断是否存在文件，不存在则爬取
                        with open(file_path, 'wb') as f:
                            content = self.get_image_content(t[1])
                            f.write(content)
                            f.close()
                            print('save success')
                except FileNotFoundError:
                    continue


def main():
    t = Pic('https://www.buxiuse.com/?', 5)
    t.download()


if __name__ == '__main__':
    main()
