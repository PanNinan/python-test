from urllib import request

# pic = requests.get('http://pics.sc.chinaz.com/files/pic/pic9/201801/zzpic9947.jpg')

if __name__ == '__main__':
    # 1
    # req = urllib.request.Request('http://www.baidu.com/')
    # response = urllib.request.urlopen(req)
    # the_page = response.read()
    # print(the_page)
    # 2
    # response = urllib.request.urlopen('http://www.baidu.com/')
    # html = response.read()

    req = request.Request('http://www.douban.com/')
    # iphone 6
    req.add_header('User-Agent',
                   'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
                   'Version/8.0 Mobile/10A5376e Safari/8536.25')
    # chrome
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/76.0.3809.100 Safari/537.36')
    with request.urlopen(req) as f:
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))
