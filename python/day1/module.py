import time

# print(dir(os))

print('-' * 30)
print(time.time())
print('-' * 30)
print(time.mktime(time.localtime()))
print('-' * 30)
print(time.strftime('%Y-%m-%d %X', time.localtime()))
print('-' * 30)
print(time.strptime('2019-05-19 18:07:35', '%Y-%m-%d %X'))
print('-' * 30)
print(time.ctime())
print('-' * 30)
print(time.asctime())
