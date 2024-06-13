import time
import random
import threading

from multiprocessing import Process

from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool
from modules.tools.thread_pools.task_pool_factory import TaskPoolFactory


def task(d1, d2, d3):
    r = random.randint(1, 10)
    time.sleep(2 / r)
    print(str(d1) + "|" + str(d2) + "|" + str(d3) + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def task2():
    print("task2")

def task3(**kwargs):
    print(kwargs)

def task_for_kwargs(**kwargs):
    print("%s|%s|%s" % (kwargs["request"], kwargs["url"], kwargs["path"]))


if __name__ == '__main__': #不加这句就会报错

    # threading.Thread(target=task_for_kwargs, kwargs={"request": "request", "url": "url", "path": "path"}).start()

    param = [
        {'name': 'name_01', 'url': 'url_01'},
        {'name': 'name_02', 'url': 'url_02'},
        {'name': 'name_03', 'url': 'url_03'}
    ]

    with TaskPoolFactory.create(10) as task_pool:
        task_pool.append(task3, param)

    '''
    TaskPool.set_count(1)
    TaskPool.append_task(Task(task_for_kwargs, kwargs={"request": "request", "path": "path", "url": "url"}))
    TaskPool.append_task(Task(task, args=('时间01:', '01d1', '01d2')))
    TaskPool.append_task(Task(task2))
    TaskPool.join()
    '''

    '''
    tasks = []
    for i in range(0, 10):
        tasks.append(Task(task, args=('时间' + str(i) + ":", str(i) + "d1", str(i) + "d2")))

    TaskPool.append_tasks(tasks)
    TaskPool.join()
    '''


