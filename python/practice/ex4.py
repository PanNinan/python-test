from bs4 import BeautifulSoup
import requests
import base64
from io import BytesIO
from PIL import Image


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # a = soup.find_all('a')
    imgs = soup.find_all('img')
    i = 1
    for img in imgs:
        img_src = img.get('src')
        if img_src.startswith('data:'):
            img_data = img_src.split(',')[1]
            binary_img_data = base64.b64decode(img_data)
            # file_like = BytesIO(binary_img_data)
            with open((str(i) + 'img.jpg'), 'wb') as f:
                f.write(binary_img_data)
            i += 1
    return ''


# 主函数
def main():
    get_html('https://image.baidu.com/')
    return


if __name__ == '__main__':
    main()
