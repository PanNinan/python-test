# 频幕跑马灯

import os
import time


def main():
    # 文本内容
    content = '红豆生南国，春来发几枝。愿君多采撷，此物最相思。'
    while True:
        # 清理频幕上的输出
        os.system('cls')
        print(content)
        time.sleep(0.4)
        # 重新组装下次要显示的文本
        content = content[1:] + content[0]


if __name__ == '__main__':
    main()
