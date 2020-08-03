import os
import requests
from bs4 import BeautifulSoup


base_url = 'https://movie.douban.com/top250?start='
base_path = os.getcwd()
self_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.106 Safari/537.36",
}


def main():
    data_list = ask_url(base_url)
    return


def ask_url(base_url):
    response = requests.get(base_url, headers=self_header)
    response.encoding = "utf-8"
    html = response.text
    bs = BeautifulSoup(html, "lxml")
    divs = bs.find_all(name="div", class_="item")
    for item in divs:
        info_url = item.find(name="a")['href']
        pic_href = item.find(name="img")['src']
        titles = item.find_all(name="span", class_="title")
        if 2 == len(titles):
            title_zh = titles[0].get_text(strip=True)
            title_en = titles[1].get_text(strip=True).replace("/", "")
        else:
            title_zh = titles[0].get_text(strip=True)
            title_en = ''
        rating_num = item.find(name="span", class_="rating_num").get_text()

        print(rating_num)
    return


def get_data():

    return


def save_data():
    return


if __name__ == '__main__':
    main()
