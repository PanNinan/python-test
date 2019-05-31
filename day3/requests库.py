from threading import Thread
from time import time
import requests


class DownloadHanlder(Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        file_name = self.url[self.url.rfind('/') + 1:]
        resp = requests.get(self.url)
        with open('./img/' + file_name, 'wb') as f:
            f.write(resp.content)


def main():
    # 606d525375387ae851b0366aa0422824
    resp = requests.get(
        'http://api.tianapi.com/meinv/?key=606d525375387ae851b0366aa0422824&num=10')
    # 将服务器返回的JSON格式的数据解析为字典
    data_model = resp.json()
    for mm_dict in data_model['newslist']:
        url = mm_dict['picUrl']
        # 通过多线程的方式实现图片下载
        DownloadHanlder(url).start()


if __name__ == '__main__':
    main()
