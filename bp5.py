# coding=utf-8
import os
import re
import sqlite3
import urllib.error
import urllib.request
import urllib.request
import urllib.robotparser

import xlwt
from bs4 import BeautifulSoup


def main():
    # 爬取网页
    base_url = 'https://movie.douban.com/top250?start='
    # 解析数据
    data_list = get_data(base_url)
    # 保存数据
    save_path = "./豆瓣电影250.xls"
    save_data_db(data_list, path=os.getcwd() + r'/movie_250')


def ask_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36",
        "Referer": "https://movie.douban.com/top250"
    }
    request = urllib.request.Request(url, headers=headers)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError:
        print('Error')
    return html


# 详情url
find_link = re.compile(r'<a href="(.*?)">')
# 图片地址
find_img_src = re.compile(r'<img.*src="(.*?)".*>', re.S)
# 标题
find_title = re.compile(r'<span class="title">(.*)</span>')
# 平均分
find_avg_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评分人数
find_rating_people = re.compile(r'<span>(\d*)人评价</span>')
# 概况
find_inq = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容
find_bd = re.compile(r'<p class="">(.*?)</p>', re.S)


def get_data(base_url):
    data_list = []
    for i in range(0, 10):
        url = base_url + str(i * 25)
        html = ask_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='item'):
            data = []
            item = str(item)
            titles = re.findall(find_title, item)
            if len(titles) == 2:
                zh_title = titles[0]
                data.append(zh_title)
                en_title = titles[1].replace('/', '')
                data.append(en_title)
            else:
                data.append(titles[0])
                data.append(' ')
            # 影片详情的链接
            link = re.findall(find_link, item)[0]
            data.append(link)
            img_src = re.findall(find_img_src, item)[0]
            data.append(img_src)
            avg_rating = re.findall(find_avg_rating, item)[0]
            data.append(avg_rating)
            rating_people = re.findall(find_rating_people, item)[0]
            data.append(rating_people)
            inqs = re.findall(find_inq, item)
            if len(inqs) != 0:
                inq = inqs[0].replace('。', '')
                data.append(inq)
            else:
                data.append(' ')
            bd = re.findall(find_bd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", '', bd)
            bd = re.sub("/", '', bd)
            data.append(bd.strip())
            data_list.append(data)
    return data_list


def save_data_xls(data_list, path):
    print('save', '-' * 50)
    work_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    work_sheet = work_book.add_sheet('豆瓣电影TOP250', cell_overwrite_ok=True)
    column = ('电影中文名称', '电影外文名称', '详情链接', '图片链接', '评分', '评价数', '概况', '相关信息')
    for i in range(0, 8):
        work_sheet.write(0, i, column[i])
    length = len(data_list)
    for i in range(0, length):
        print('第%d条' % (i + 1))
        for j in range(0, 8):
            work_sheet.write((i + 1), j, data_list[i][j])
    s = os.getcwd()
    work_book.save(s + r'/豆瓣电影Top250.xls')
    print('success', '-' * 50)


def save_data_db(data_list, path):
    init_db(path)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    for data in data_list:
        for index in range(len(data)):
            if index == 5 or index == 4:
                continue
            else:
                data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie_250 (
                name_zh, name_en, info_link, pic_link,score,rated,instroduction, info
            ) values (%s)''' % ",".join(data)
        conn.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()
    return


def init_db(path):
    sql = '''
        create table movie_250 
        (
        id integer primary key autoincrement,
        name_zh varchar,
        name_en varchar,
        info_link varchar,
        pic_link varchar,
        score numeric ,
        rated numeric ,
        instroduction text,
        info text
        )
    '''
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    main()
