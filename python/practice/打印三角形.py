"""
    打印三角形
"""

'''
    *
    **
    ***
    ****
'''


def print_l():
    row = int(input('请输入需要打印的三角形的行数: '))
    print('-' * 20 + '开始打印' + '-' * 20)
    for r in range(row):  # 控制行数
        for i in range(r + 1):  # 控制打印*数
            print('*', end='')
        print()
    print('-' * 20 + '打印结束' + '-' * 20)


'''
       *
      **
     ***
    ****
'''


def print_r():
    row = int(input('请输入需要打印的三角形的行数: '))
    print('-' * 20 + '开始打印' + '-' * 20)
    for r in range(row):  # 控制行数
        for i in range(row):  # 控制打印*数
            if row - r - 1 > i:
                print(' ', end='')
            else:
                print('*', end='')
        print()
    print('-' * 20 + '打印结束' + '-' * 20)


if __name__ == '__main__':
    print_r()
