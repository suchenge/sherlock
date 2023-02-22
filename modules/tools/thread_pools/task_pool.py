import threading
import queue

from threading import Lock
from modules.tools.thread_pools.task import Task


class TaskPool(object):
    __queue__ = queue.Queue()
    __stop__ = False
    __created__ = False
    __count__ = 10
    __threads__ = []
    __lock__ = Lock()

    @staticmethod
    def __build__():
        if TaskPool.__created__ is False:
            TaskPool.__lock__.acquire()

            if TaskPool.__created__ is False:
                for i in range(0, TaskPool.__count__):
                    TaskPool.__threads__.append(threading.Thread(target=TaskPool.__task_executor__, args=str(i)))

                for thread in TaskPool.__threads__:
                    thread.start()

                TaskPool.__created__ = True

            TaskPool.__lock__.release()

    @staticmethod
    def join():
        print("等待所有线程完成")

        TaskPool.__stop__ = True

        for thread in TaskPool.__threads__:
            thread.join()

        TaskPool.__created__ = False
        TaskPool.__threads__ = []

        print("所有线程都结束了")

    @staticmethod
    def set_count(value: int):
        TaskPool.__count__ = value

    @staticmethod
    def stop():
        TaskPool.__stop__ = True

    @staticmethod
    def __get_task__() -> Task:
        task = None
        # TaskPool.__lock__.acquire()
        task = TaskPool.__queue__.get()
        # TaskPool.__lock__.release()

        return task

    @staticmethod
    def __task_executor__(thread_id):
        while True:
            task = TaskPool.__get_task__()
            if task is not None:
                task.run()

            if TaskPool.__queue__.empty() and TaskPool.__stop__ is True:
                print("线程[" + thread_id + "] break")
                break

        print("线程[" + thread_id + "]结束运行")

    @staticmethod
    def append_task(task: Task):
        TaskPool.__stop__ = False
        TaskPool.__queue__.put(task)
        TaskPool.__build__()

    @staticmethod
    def append_tasks(tasks: []):
        for task in tasks:
            TaskPool.append_task(task)
