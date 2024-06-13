from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool


class TaskPoolManager(object):
    def __init__(self, max_workers=10):
        TaskPool.set_count(max_workers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        TaskPool.join()

    def append(self, executor, iterables):
        for args in iterables:
            TaskPool.append_task(Task(executor, kwargs=args))
