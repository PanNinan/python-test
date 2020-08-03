# 类


class Person:
    version = '0.1.0'
    name = ''
    age = 0
    sex = ''

    def __init__(self, name, age, sex):
        """ 类初始化方法 """
        self.name = name
        self._age = age
        self.sex = sex

    def des(self):
        """这里是形容函数"""
        print('这里是一个人的类,姓名是%s, 年龄为%d, 性别为%s' % (self.name, self.age, self.sex))

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @classmethod
    def class_des(cls):
        print('这是一个人的类')

    @staticmethod
    def class_static_m():
        print('这是一个静态方法')


p = Person('panninan', 26, 'man')
p.age = 25
print(p)
Person.version = '0.2.0'
print(p.version)
print(p.__dict__)
print(p.__doc__)
print(p.__module__)
print(p.name)
p.des()

print(dir(Person))
