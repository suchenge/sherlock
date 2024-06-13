from modules.tools.thread_pools.task_pool_manager import TaskPoolManager

class TaskPoolFactory(object):
    @staticmethod
    def create(max_workers=10):
        return TaskPoolManager(max_workers)
