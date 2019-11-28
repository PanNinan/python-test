import requests
import re
import os


search_key = input("请输入关键字\n")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
           'Referer': 'https://www.mzitu.com/'}


response = requests.get('https://www.mzitu.com/search/' +
                        search_key+'/', headers=headers)
image_field = re.findall(
    '<div class="postlist">([\s\S]*?)<nav class="navigation pagination" role="navigation">', response.text)

# 1.找到每个图片的链接
img_hrefs = re.findall('<li><a href="(.*?)"', image_field[0])
name_list = re.findall("alt='(.*?)'", image_field[0])


for n in range(len(img_hrefs)):

    # 2.创建对应的文件夹
    dir_name = name_list[n].replace(' ', '')

    if not os.path.exists('./girl_images/' + dir_name):
        os.mkdir('./girl_images/'+dir_name)

    # 3.进入链接,并找到页数
    detail_response = requests.get(img_hrefs[n], headers=headers)
    tmp_text = re.findall(
        '<div class="pagenavi">([\s\S]*?)</div>', detail_response.text)
    page_list = re.findall('<span>(\d*?)</span>', tmp_text[0])
    page_count = int(page_list[-1])

    # 4.获取该图集的每一个链接
    for page in range(1, page_count+1):
        page_url = img_hrefs[n]+'/'+str(page)
        page_response = requests.get(page_url, headers=headers)
        page_field = re.findall(
            '<div class="main-image">([\s\S]*?)</div>', page_response.text)
        main_image_url_list = re.findall('<img src="(.*?)"', page_field[0])

        with open('./girl_images/' + dir_name+'/' + str(page)+'.jpg', 'wb') as image:
            image.write(requests.get(
                main_image_url_list[0], headers=headers).content)
