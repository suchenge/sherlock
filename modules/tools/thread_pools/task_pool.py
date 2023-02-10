import threading
import queue
from modules.tools.thread_pools.task import Task


class TaskPool(object):
    __queue__ = queue.Queue()
    __stop__ = False
    __created__ = False
    __count__ = 10

    @staticmethod
    def __build__():

        TaskPool.__created__ = True

        threads = []

        for i in range(0, TaskPool.__count__):
            threads.append(threading.Thread(target=TaskPool.__task_executor__))

        for thread in threads:
            thread.start()

    @staticmethod
    def set_count(value: int):
        TaskPool.__count__ = value

    @staticmethod
    def stop():
        TaskPool.__stop__ = True

    @staticmethod
    def __get_task__() -> Task:
        return TaskPool.__queue__.get()

    @staticmethod
    def __task_executor__():
        # print("\n线程[" + thread_id + "]开始运行")

        while True:
            task = TaskPool.__get_task__()
            if task is not None:
                task.run()

            # if TaskPool.__stop__ is True:
                # print("\nstoped, qsize:" + str(TaskPool.__queue__.qsize()))

            if TaskPool.__queue__.empty() and TaskPool.__stop__ is True:
                # print("\n" + str(TaskPool.__stop__))
                break

        # print("\n线程[" + thread_id + "]完成运行")

    @staticmethod
    def append_task(task: Task):
        TaskPool.__stop__ = False
        TaskPool.__queue__.put(task)
        if TaskPool.__created__ is False:
            TaskPool.__build__()

    @staticmethod
    def append_tasks(tasks: []):
        for task in tasks:
            TaskPool.append_task(task)
