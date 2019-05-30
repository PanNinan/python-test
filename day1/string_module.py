string = 'my name is %s %d %s' % ('ninan', 2, [1, 2, 3])

# print(string)

tpl = 'I am %(name)s, my age is %(age)d' % {"name": "ninan", "age": 25}


# print(tpl)


def test(x, *args, **kargs):
    x = 2 * x + 1
    print(args)
    print(kargs)
    return x


t1 = test(0.01, *[1, 2, 3, 4], **{'a': 1, 'b': 2, 'c': 3, 'd': 4})

print(t1)
