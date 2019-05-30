import time
from abc import ABCMeta
from random import randint, randrange


class Fighter(object, metaclass=ABCMeta):
    """战斗者"""

    # 通过__slots__限定绑定对象可绑定的成员变量
    __slots__ = ('_name', '_hp')

    def __init__(self, name, hp):
        """

        :param name: 名字
        :param hp: 生命值
        """
        self._name = name
        self._hp = hp

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp

    @property
    def alive(self):
        return self._hp > 0

    def attack(self, other):
        """

        :param other: 被攻击对象
        """
        pass


class Ultraman(Fighter):
    """奥特曼"""

    __slots__ = ('_name', '_hp', '_mp')

    def __init__(self, name, hp, mp):
        """
        初始化
        :param name: 名字
        :param hp:  生命值
        :param mp:  魔法值
        """
        super().__init__(name, hp)
        self._mp = mp

    def attack(self, other):
        """
        普通攻击
        :param other: 被攻击对象
        :return:
        """
        other.hp -= randint(10, 20)

    def hug_attack(self, other):
        """
        大招 [若成功发出,则打掉对方至少50或者四分之三的hp]
        :param other:
        :return:
        """
        if self._mp >= 50:
            self._mp -= 50
            hurt = other.hp * 3 / 4
            hurt = hurt if hurt > 50 else 50
            other.hp -= hurt
            return True
        else:
            self.attack(other)
            return False

    def magic_attack(self, others):
        """
        魔法攻击 [群体攻击 对每个单体造成10-15随机伤害]
        :param others:
        :return:
        """
        if self._mp >= 20:
            self._mp -= 20
            for tmp in others:
                if tmp.alive:
                    tmp.hp -= randint(10, 15)
            return True
        else:
            return False

    def resume(self):
        """
        回复mp
        :return: 回复点数
        """
        restore = randint(1, 10)
        self._mp += restore
        return restore

    def __str__(self):
        return '~~~%s奥特曼~~~\n' % self._name + 'HP: %d\n' % self._hp + 'MP: %d\n' % self._mp


class Monster(Fighter):
    """小怪兽"""

    def attack(self, other):
        """
        普通攻击
        :param other: 被击对象
        :return: 随机造成10-20点伤害
        """
        other.hp -= randint(10, 20)

    def __str__(self):
        return '~~~%s小怪兽~~~\n' % self._name + 'HP: %d\n' % self._hp


def is_any_alive(monsters):
    """判断有没有小怪兽活着"""
    for monster in monsters:
        if monster.alive:
            return True
    return False


def select_alive_one(monsters):
    """
    选择一个活着的小怪兽
    :param monsters: 怪兽组
    :return: 随机的活着的怪兽
    """
    num = len(monsters)
    while True:
        index = randrange(num)
        monster = monsters[index]
        if monster.alive:
            return monster


def display_info(ultraman, monsters):
    """打印奥特曼和小怪兽的信息"""
    print(ultraman)
    for monster in monsters:
        print(monster, end='')


def main():
    """
    奥特曼VS怪兽组合
    攻击方式  60%的概率使用普通攻击,普通攻击会回复mp
            30%的概率使用魔法攻击(可能因魔法值不足而失败)
            10%的概率使用究极必杀技(如果魔法值不足则使用普通攻击)
    """
    u = Ultraman('赛文', 200, 100)
    m1 = Monster('盖欧扎克', 100)
    m2 = Monster('丸迫奈扎', 100)
    m3 = Monster('奥古玛', 100)
    ms = [m1, m2, m3]
    fight_round = 1
    while u.alive and is_any_alive(ms):
        print('第%d回合'.center(50, '=') % fight_round)
        m = select_alive_one(ms)
        skill = randint(1, 10)
        if skill <= 6:
            print('%s使用普通攻击命中%s' % (u.name, m.name))
            u.attack(m)
            print('%s回复了%d点mp' % (u.name, u.resume()))
        elif skill <= 9:
            if u.magic_attack(ms):
                print('%s使用了魔法攻击' % u.name)
            else:
                print('%s使用魔法失败.' % u.name)
        else:
            if u.hug_attack(m):
                print('%s成功释放大招命中%s' % (u.name, m.name))
            else:
                print('%s使用普通攻击命中%s.' % (u.name, m.name))
                print('%s的魔法值恢复%d点.' % (u.name, u.resume()))
        if m.alive:  # 小怪兽没死,就反击
            print('%s回击了%s' % (u.name, m.name))
            m.attack(u)
        display_info(u, ms)  # 一回合结束,显示奥特曼和小怪兽们的信息
        fight_round += 1
        time.sleep(1)
    print('\n==========战斗结束,共%d回合==========\n' % (fight_round - 1))
    if u.alive:
        print('%s获得胜利!' % u.name)
    else:
        print('小怪兽获得胜利!')


if __name__ == '__main__':
    main()
