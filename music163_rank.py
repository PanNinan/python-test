import os
import re
import time

import requests
import xlwt
from bs4 import BeautifulSoup

base_url = 'https://music.163.com/#/discover/toplist?id=3778678'
base_path = os.getcwd()
self_header = {
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.106 Safari/537.36",
    "referer": "https://music.163.com/",
    "cookie": "JSESSIONID-WYYY=WgYwFFvU0BSBnfkbdVAryWVmEWxR%2BOzzXPxrnMgjtiqGlQhPS%2BBEU99ZVYC6Vyjfs%2BfzhzvU4B4"
              "%2FOYPM%2BrrYWF59fog0qSPwY6p0CxvMYP667l%2B2528hIgcQHqnkUbxUg7v3n"
              "%5CcqXpzwicWiA70iuW0GAbY6y8dOIrhC82cfvj9J7hRS%3A1596444744344; _iuqxldmzr_=32; "
              "_ntes_nnid=6e655480f61bd2c16d5d477607f254c8,1596442944391; "
              "_ntes_nuid=6e655480f61bd2c16d5d477607f254c8; "
              "WM_NI=YWEwaPGS1or50pJ64sM2pOP75VQbQ"
              "%2BXhSa1M3D5OpfOgHhogl75TgXxznztzgwpbDfINdtR4lm4AvXfBTtZZAUWuikpBSzhcFdQOvXc2F0r4oKe2NxWJnrHRED9a8YiCOUg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee82c25fb5e98790d14d8b9e8fa3d84a939f8a85b554ade7abadd06d9aa999aded2af0fea7c3b92a9b898b98e45c858dff90f13ff4b086d7b7798feec0b0d33df78a9f83d4219cb89d82b447f19cfbb0f36e8db98889ee6db0e9fbb5e654bca6a29bf772a5a9c083c76e8b92ac95d140b0b3fca2f554a69e9c95d952838b9996ec61b49e9d9beb6986bc9fb0f554a1ee8ad1f140ad95abd3cd749596a293cb5a879cf782bb53ab9d81b6e637e2a3; WM_TID=TWkOqwpiA7dABFVUQBYqHpsePcwJhWOn; MUSIC_U=340de69b0634dda7671a78571e0c19ab3e397a032acffac74edf457b5af00a6133a649814e309366; __csrf=61ae48a1a38847ed64dd9b203525f563; ntes_kaola_ad=1 "
}


def get_data_from_url(url):
    response = requests.get(url, headers=self_header)
    response.encoding = "utf-8"
    content = response.text
    bs = BeautifulSoup(content, 'lxml')
    table = bs.find(name="table", class_="m-table-rank")
    print(content)


if __name__ == '__main__':
    get_data_from_url(base_url)
