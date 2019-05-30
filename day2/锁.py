# 加锁的线程

from threading import Lock, Thread
from time import sleep


class Account(object):

    def __init__(self, balance=0):
        self._balance = balance
        self._lock = Lock()

    def deposit(self, money):
        # 先取锁
        self._lock.acquire()
        try:
            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
        finally:
            self._lock.release()

    @property
    def balance(self):
        return self._balance


class AddMoneyThread(Thread):

    def __init__(self, account, money):
        super(AddMoneyThread, self).__init__()
        self._account = account
        self._money = money

    def run(self):
        self._account.deposit(self._money)


def main():
    account = Account(0)
    threads = []
    for _ in range(100):
        t = AddMoneyThread(account, 1)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print('账户余额为%d元' % account.balance)


if __name__ == '__main__':
    main()
