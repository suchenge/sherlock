import threading
import queue
import time
import re

from threading import Lock

from modules.tools.thread_pools.task import Task


def __get_method_description__(task: Task):
    method_info = str(task.__method__)
    try:
        match = re.compile(r"<bound method (.*) of.*?").findall(method_info)
        if match:
            return match[0]
    except Exception as error:
        pass
    return ""


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
                    TaskPool.__threads__.append(threading.Thread(target=TaskPool.__task_executor__, args=[str(i)]))

                for thread in TaskPool.__threads__:
                    thread.start()

                TaskPool.__created__ = True

            TaskPool.__lock__.release()

    @staticmethod
    def join():
        TaskPool.stop()

        for thread in TaskPool.__threads__:
            thread.join()

        TaskPool.__created__ = False
        TaskPool.__threads__ = []

        print("所有线程都结束了")

    @staticmethod
    def set_count(value: int):
        TaskPool.__count__ = value



    @staticmethod
    def stop(stop=True):
        TaskPool.__lock__.acquire()

        if not TaskPool.__stop__:
            TaskPool.__stop__ = stop

        TaskPool.__lock__.release()

    @staticmethod
    def __get_task__() -> Task:
        task = None
        TaskPool.__lock__.acquire()

        if not TaskPool.__queue__.empty():
            task = TaskPool.__queue__.get()

        TaskPool.__lock__.release()

        return task

    @staticmethod
    def __task_executor__(thread_id):
        while True:
            task = TaskPool.__get_task__()

            if task is not None:
                # print("线程[" + thread_id + "][" + str(time.time()) + "] run " + __get_method_description__(task) + "")
                task.run()

            if TaskPool.__queue__.empty() and TaskPool.__stop__ is True:
                print("线程[" + thread_id + "][" + str(time.time()) + "] 结束运行")
                break

    @staticmethod
    def append_task(task: Task):
        if task.in_queue_delay_seconds > 0:
            delay_thread = threading.Thread(target=TaskPool.__delay_in_queue__, args=[task])
            delay_thread.start()
        else:
            TaskPool.__in_queue__(task)

    @staticmethod
    def __delay_in_queue__(task: Task):
        time.sleep(task.in_queue_delay_seconds)
        TaskPool.__in_queue__(task)

    @staticmethod
    def __in_queue__(task: Task):
        TaskPool.stop(False)
        TaskPool.__queue__.put(task)
        TaskPool.__build__()

    @staticmethod
    def append_tasks(tasks: []):
        for task in tasks:
            TaskPool.append_task(task)
