# 生成器 迭代器 三元表达式

list1 = ('第%d个元素' % i for i in range(20) if i % 3 == 0)  # 生成器表达式
list2 = ['第%d个元素' % i for i in range(20) if i % 3 == 0]  # 列表解析

print(list1)
print(list2)

print(next(list1))
print(list1.__next__())
