import threading
import queue


class ThreadPool(object):
    def __init__(self, tasks, parallel_count=10):
        self.__queue__ = queue.Queue()

        for task in tasks:
            self.__queue__.put(task)

        self.__parallel_count__ = parallel_count

    def __task_executor__(self):
        while not self.__queue__.empty():
            task = self.__queue__.get()

            if task is not None:
                task['executor'](task['args'])

    def __thread_executor__(self):
        return threading.Thread(target=self.__task_executor__)

    def execute(self):
        count = self.__parallel_count__
        if self.__queue__.qsize() < count:
            count = self.__queue__.qsize()

        executors = [self.__thread_executor__() for i in range(0, count)]

        for executor in executors:
            executor.start()

        for executor in executors:
            executor.join()
