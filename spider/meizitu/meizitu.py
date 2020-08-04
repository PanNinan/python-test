import os

import requests
from bs4 import BeautifulSoup


def mkdir(path):  # 这个函数创建文件夹
    path = path.strip()
    is_exists = os.path.exists(os.path.join(r"D:\mzitu", path))
    if not is_exists:
        print(u'新建文件夹：', path)
        os.makedirs(os.path.join(r"D:\mzitu", path))
        os.chdir(os.path.join(r"D:\mzitu", path))  # 切换到目录
        return True
    else:
        print(u'文件夹 ', path, u'已存在，跳过')
        return False


class mzitu():

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
                          "Chrome/19.0.1055.1 Safari/535.24",
            'Referrer': 'www.mzitu.com'
        }

    def all_url(self, url):
        html = self.request(url)  # 调用request函数把套图地址传进去会返回给我们一个response
        all_a = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='all').find_all('a')

        for a in all_a:
            title = a.get_text()
            old = '早期图片'
            if title == old:
                continue
            print(u'开始保存：', title)
            # 我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            path = str(title).replace("?", '_')
            if mkdir(path) is not True:
                continue
            href = a['href']
            self.html(href)

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

    def request(self, url):
        content = requests.get(url, headers=self.headers)
        return content


if __name__ == "__main__":
    Mzitu = mzitu()
    Mzitu.all_url('https://www.mzitu.com/all/')
