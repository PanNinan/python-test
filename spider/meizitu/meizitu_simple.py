import os

import requests
from bs4 import BeautifulSoup


class mzitu():

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
                          "Chrome/19.0.1055.1 Safari/535.24",
            'Referer': 'https://www.mzitu.com'
        }

    def all_url(self, url):
        self.headers['Referer'] = url;
        html = self.request(url)  # 调用request函数把套图地址传进去会返回给我们一个response
        # title
        title = BeautifulSoup(html.text, 'lxml').find(
            'h2', class_='main-title').get_text()
        print(u'开始保存：', title)
        # 我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
        path = str(title).replace("?", '_')
        self.mkdir(path)  # 调用mkdir函数创建文件夹！这儿path代表的是标题title
        # 获取底部分页栏
        pagenavi = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='pagenavi').find_all('a')
        # 最后一页的a标签
        last_a = pagenavi[-2]
        # 最后一页页码数
        last_num = last_a.find('span').text
        for page in range(1, int(last_num) + 1):
            page_url = url + '/' + str(page)
            self.img(page_url)  # 调用img函数

    def html(self, href):  # 这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)
        self.headers['referer'] = href
        max_span = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)  # 调用img函数

    def img(self, page_url):  # 这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find(
            'div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):  # 这个函数保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
        print("%s保存完成！" % name)

    def mkdir(self, path):  # 这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'新建文件夹：', path)
            os.makedirs(os.path.join("D:\mzitu", path))
            os.chdir(os.path.join("D:\mzitu", path))  # 切换到目录
            return True
        else:
            return False

    def request(self, url):
        content = requests.get(url, headers=self.headers)
        return content


Mzitu = mzitu()
Mzitu.all_url('https://www.mzitu.com/62939')
