import re

"""
    原字符:
    .  占位
    $  结尾
    ^  开头
    *  0-无穷个
    +  1-无穷个
    {} 自定义个数范围
    [] [0-9] 0-9的数字 [a-z] a-z的字母 [^1234]除了1234
    |  
    ()  
    \  
"""

temp_str = 'a12b123b\\6qwbE98Wwwwwwwwee8qwyeqjweqwu8u0'

all_num = re.findall('\d', temp_str)

res = re.findall('\d+', temp_str)

res1 = re.findall('a..b', temp_str)

res2 = re.findall('w*', temp_str)  # 匹配0到无穷次

res3 = re.findall('w+', temp_str)  # 匹配1到无穷次

res4 = re.findall('ww+?e', temp_str)

res5 = re.findall('w{1,7}e+', temp_str)

res6 = re.findall('q[a-zA-Z]*', temp_str)

res7 = re.findall('e8|8u', temp_str)

print(all_num)
print(res)
print(res1)
print(res2)
print(res3)
print(res4)
print(res5)
print(res6)
print(res7)
