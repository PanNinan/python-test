# 文件操作:写

from math import sqrt


def is_prime(n):
    """判断素数的函数"""
    assert n > 0
    for item in range(2, int(sqrt(n) + 1)):
        if n % item == 0:
            return False
    return True if n != 1 else False


def main():
    """将1-10000中的素数分别写入a b c 三个文件"""
    filenames = ['./file/a.txt', './file/b.txt', './file/c.txt']
    fs_list = []
    count = 0
    try:
        for filename in filenames:
            fs_list.append(open(filename, 'w', encoding='utf-8'))
        for number in range(1, 10000):
            if is_prime(number):
                count += 1
                if number < 3000:
                    fs_list[0].write(str(number) + '\n')
                elif number < 6000:
                    fs_list[1].write(str(number) + '\n')
                else:
                    fs_list[2].write(str(number) + '\n')
    except IOError as ex:
        print(ex)
        print('写文件时发生错误!')
    finally:
        for fs in fs_list:
            fs.close()
    print('操作完成!总共%d个素数' % count)


if __name__ == '__main__':
    main()
