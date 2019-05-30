# 文件操作
import time

# 复制
with open('music', encoding='utf-8') as f, open('music_copy', 'a', encoding='utf-8') as fw:
    if f.readable():
        data = f.read()
        if data:
            fw.write(data + '\r\n')
    else:
        print('this file can not read!')
f.close()
fw.close()

with open('music', encoding='utf-8') as f:
    for line in f:
        print(line)
        time.sleep(1)
