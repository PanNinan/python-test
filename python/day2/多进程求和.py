from multiprocessing import Process, Queue
from time import time


def task_handler(curr_list, result_queue):
    total = 0
    for number in curr_list:
        total += number
    return result_queue.put(total)


def main():
    processes = []
    number_list = range(1, 100000001)
    result_queue = Queue()
    index = 0
    # 启动8个进程,将数据切片后计算
    for _ in range(8):
        p = Process(target=task_handler, args=(
            number_list[index:index + 12500000], result_queue))
        index += 12500000
        processes.append(p)
        p.start()
    # 记录所有进程计算完花费的时间
    start = time()
    for process in processes:
        process.join()
    # 执行合并结果
    total = 0
    while not result_queue.empty():
        total += result_queue.get()
    print(total)
    end = time()
    print('耗时: %.2f秒' % (end - start))


if __name__ == '__main__':
    main()
