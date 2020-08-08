class Test:
    def __init__(self, foo):
        self.__foo = foo

    def __bar(self):
        print(self.__foo)
        print('__bar')


class Person(object):
    # 限定Person对象只能绑定_name, _age和_gender属性
    __slots__ = ('_name', '_age', '_gender')

    def __init__(self, name, age):
        self._name = name
        self._age = age

    # 访问器 - getter 方法
    @property
    def name(self):
        return self._name

    # 访问器 - getter 方法
    @property
    def age(self):
        return self._age

    # 修改器 - setter方法
    @age.setter
    def age(self, age):
        self._age = age

    def play(self):
        if self._age < 18:
            print('%s正在玩飞行棋.' % self._name)
        else:
            print('%s正在玩斗地主' % self._name)


def main():
    test = Test('hello')
    # test.__bar()  # 不可访问
    # print(test.__foo)  # 不可访问
    test._Test__bar()  # 可以访问
    print(test._Test__foo)  # 可以访问
    John = Person('John', 16)
    John_name = John.name
    print(John_name)
    John.age = 18
    # John.name = 'John-117' # can't set attribute
    John.play()


if __name__ == '__main__':
    main()
