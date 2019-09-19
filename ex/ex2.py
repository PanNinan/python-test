import requests
import urllib.request
import re  # 正则匹配目标文件
import os
import urllib

pic = requests.get('http://pics.sc.chinaz.com/files/pic/pic9/201801/zzpic9947.jpg')

if __name__ == '__main__':
    with open('picfile.jpg', 'wb') as f:
        f.write(pic.content)
