from abc import ABCMeta, abstractmethod
from random import randint, randrange


class Fighter(object, metaclass=ABCMeta):
    __slots__ = ('_name', '_hp')

    def __init__(self, name, hp):
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

    @abstractmethod
    def attack(self, other):
        ...


class Ultraman(Fighter):
    __slots__ = ('_name', '_hp', '_mp')

    def __init__(self, name, hp, mp):
        super().__init__(name, hp)
        self._mp = mp

    @property
    def mp(self):
        return self._mp

    @mp.setter
    def mp(self, mp):
        self._mp = mp

    def attack(self, other):
        hurt = randint(10, 25)
        other.hp -= hurt
        return hurt

    def magic_attack(self, others):
        if self.mp >= 20:
            self.mp -= 20
            hurt = randint(15, 20)
            for other in others:
                if other.alive:
                    other.hp -= hurt
            return True
        else:
            return False

    def resume(self):
        """恢复魔法值"""
        incr_point = randint(1, 10)
        self._mp += incr_point
        return incr_point

    def hug_attack(self, other):
        if self.mp >= 20:
            self.mp -= 20
            hurt = other.hp * 4 / 5
            hurt = hurt if hurt > 50 else 50
            other.hp -= hurt
            return True
        else:
            return False

    def __str__(self):
        return '~~~%s~~~\n' % self.name + 'HP: %d   MP: %d\n' % (self.hp, self.mp)


class Monster(Fighter):

    def attack(self, other):
        hurt = randint(15, 25)
        other.hp -= hurt
        return hurt

    def __str__(self):
        return '~~~%s~~~\n' % self.name + 'HP: %d\n' % self.hp


def is_any_alive(monsters):
    for monster in monsters:
        if monster.alive:
            return True
    return False


def select_a_monster(monsters):
    num = len(monsters)
    while True:
        index = randrange(num)
        monster = monsters[index]
        if monster.alive:
            return monster


def display_info(ultraman, monsters):
    print(ultraman)
    for monster in monsters:
        print(monster, end='')


def main():
    u = Ultraman('迪迦', 200, 60)
    m1 = Monster('加坦杰厄', 100)
    m2 = Monster('贝利亚', 100)
    m3 = Monster('黑暗扎基', 100)
    ms = [m1, m2, m3]
    fight_round = 1
    while u.alive and is_any_alive(ms):
        print('第%d回合开始'.center(50, '*') % fight_round)
        m = select_a_monster(ms)  # 选取一只有效怪兽
        print('小怪兽%s出场\n' % m.name)
        skill = randint(1, 100)
        if skill <= 60:
            print('%s使用普通攻击命中%s 造成%d点伤害 回复%d点MP' % (u.name, m.name, u.attack(m), u.resume()))
        elif skill <= 90:
            if u.magic_attack(ms):
                print('%s释放魔法攻击 造成大量范围伤害' % u.name)
            else:
                print('%s因MP不足释放魔法攻击失败[MP=%d] 使用普通攻击命中%s 造成%d点伤害回复%d点MP' % (
                    u.name, u.mp, m.name, u.attack(m), u.resume()))
        else:
            if u.hug_attack(m):
                print('%s释放超大招命中%s 造成大量单体伤害' % (u.name, m.name))
            else:
                print(
                    '%s因MP不足释放超大招失败[MP=%d] 使用普通攻击命中%s 造成%d点伤害回复%d点MP' % (u.name, u.mp, m.name, u.attack(m), u.resume()))
        if m.alive:
            print('%s使用普通攻反击 攻击命中%s 造成%d点伤害' % (m.name, u.name, m.attack(u)))
        else:
            print('%s死亡' % m.name)
        display_info(u, ms)
        fight_round += 1
        print('回合结束'.center(50, '*') + '\n')
    print('战斗结束!'.center(50, '*'))
    if u.alive:
        print('%s胜利!' % u.name)
    else:
        print('小怪兽胜利!')


if __name__ == '__main__':
    main()
