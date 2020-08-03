# 用二进制读写文件实现图片复制


def main():
    file_name = './file/time1.jpg'
    dis_name = './file/time.jpg'
    try:
        with open(file_name, 'rb') as fs1:
            data = fs1.read()
            print(type(data))
        with open(dis_name, 'wb') as fs2:
            fs2.write(data)
    except FileNotFoundError:
        print('无法打开')
    except IOError:
        print('读写出现错误!')
    finally:
        print('执行结束')


if __name__ == '__main__':
    main()
