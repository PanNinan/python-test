# 文件操作:读
import time


def main():
    try:
        with open('./file/静夜思.txt', 'r', encoding='utf-8') as f:
            # 一次性读取整个文件内容
            print(f.read())
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('未知编码')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        ...


def main1():
    try:
        with open('./file/静夜思.txt', 'r', encoding='utf-8') as f:
            # 通过for-in循环逐行读取
            for line in f:
                print(line, end='')
                time.sleep(0.5)
            print()
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('未知编码')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        ...


def main2():
    try:
        with open('./file/静夜思.txt', 'r', encoding='utf-8') as f:
            # 读取文件按行读取到列表中
            lines = f.readlines()
            print(lines)
            for line in lines:
                print(line, end='')
            print()
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('未知编码')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        ...


if __name__ == '__main__':
    main2()
