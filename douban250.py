import os
import re
import requests
import xlwt
from bs4 import BeautifulSoup

base_url = 'https://movie.douban.com/top250?start='
base_path = os.getcwd()
self_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.106 Safari/537.36",
}


def main():
    data_list = ask_url_for_data()
    save_path = base_path + r'/tmp/'
    save_data(data_list, save_path, 'xls')
    return


def ask_url_for_data():
    # 循环请求分页页面
    data_list = []
    for i in range(0, 26):
        url = base_url + str(i * 10)
        data = get_single_page_data(url)
        data_list += data
    return data_list


def get_single_page_data(url):
    page_data = []
    response = requests.get(url, headers=self_header)
    response.encoding = "utf-8"
    html = response.text
    bs = BeautifulSoup(html, "lxml")
    divs = bs.find_all(name="div", class_="item")
    for item in divs:
        data = []
        titles = item.find_all(name="span", class_="title")
        if 2 == len(titles):
            title_zh = titles[0].get_text(strip=True)
            title_en = titles[1].get_text(strip=True).replace("/", "")
        else:
            title_zh = titles[0].get_text(strip=True)
            title_en = ''
        data.append(title_zh)
        data.append(title_en)
        pic_href = item.find(name="img")['src']
        data.append(pic_href)
        info_url = item.find(name="a")['href']
        data.append(info_url)
        rating_num = item.find(name="span", class_="rating_num").get_text()
        data.append(rating_num)
        rate_person = item.select(".star span")[-1].get_text()
        rate_person_num = re.findall(r"\d+\.?\d*", rate_person)[0]
        data.append(rate_person_num)
        inq = item.find(name="span", class_="inq")
        if inq is not None:
            inq = inq.get_text(strip=True)
        else:
            inq = ''
        data.append(inq)
        summary = item.find(name="div", class_="bd").p.get_text(strip=True)
        data.append(summary)
        page_data.append(data)
    return page_data


def save_data(data_list, save_path, save_type='xls'):
    create_dir(save_path)
    if 'xls' == save_type:
        save2xls(data_list, save_path)
    elif 'db' == save_type:
        save2db(data_list, save_path)
    elif 'redis' == save_type:
        save2redis(data_list, save_path)
    return


def save2xls(data_list, save_path):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('豆瓣电影TOP250')
    # 写入表头信息
    xls_head = ['中文名称', '外文名称', '图片', '详情链接', '评分', '参评人数', '概括', '简介']
    for index, head in enumerate(xls_head):
        worksheet.write(0, index, head)
    for i, item in enumerate(data_list):
        tmp_data = data_list[i]
        for j, value in enumerate(tmp_data):
            worksheet.write(i + 1, j, value)
    workbook.save(save_path + '\\豆瓣电影TOP250.xls')


def save2db(data_list, save_path):
    return


def save2redis(data_list, save_path):
    return


def create_dir(save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)


if __name__ == '__main__':
    main()
