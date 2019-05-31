# 列表中最大和第二大的元素的值


def main(l):
    m1, m2 = (l[0], l[1]) if l[0] > l[1] else (l[1], l[0])
    for index in range(2, len(l)):
        if l[index] > m1:
            m2 = m1
            m1 = l[index]
        elif l[index] > m2:
            m2 = l[index]
    return m1, m2


if __name__ == '__main__':
    l = [2, 3, 4, 6, 7, 1, 3, 6, 8, 2, 13, 4, 9, 10]
    print(main(l))
