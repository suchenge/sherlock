import time
import random
import threading

from multiprocessing import Process

from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool


def task(d1, d2, d3):
    r = random.randint(1, 10)
    time.sleep(2 / r)
    print(str(d1) + "|" + str(d2) + "|" + str(d3) + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def task2():
    print("task2")


def task_for_kwargs(**kwargs):
    print("%s|%s|%s" % (kwargs["request"], kwargs["url"], kwargs["path"]))


if __name__ == '__main__': #不加这句就会报错

    # threading.Thread(target=task_for_kwargs, kwargs={"request": "request", "url": "url", "path": "path"}).start()

    TaskPool.set_count(1)
    TaskPool.append_task(Task(task_for_kwargs, kwargs={"request": "request", "path": "path", "url": "url"}))
    TaskPool.append_task(Task(task, args=('时间01:', '01d1', '01d2')))
    TaskPool.append_task(Task(task2))

    # tasks = []
    # for i in range(0, 10):
    #     tasks.append(Task(task, args=('时间' + str(i) + ":", str(i) + "d1", str(i) + "d2")))

    # TaskPool.append_tasks(tasks)

    TaskPool.join()
