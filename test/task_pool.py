import time
import random

from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool


def task(args):
    r = random.randint(1, 10)
    time.sleep(2 / r)
    # print(str(args) + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


TaskPool.set_count(10)
TaskPool.append_task(Task(task, '时间01:'))
TaskPool.append_task(Task(task, '时间02:'))

tasks = []
for i in range(0, 100):
    tasks.append(Task(task, '时间' + str(i) + ":"))

TaskPool.append_tasks(tasks)

TaskPool.stop()
