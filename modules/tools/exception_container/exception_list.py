import queue

from modules.framework.decorators.base_decorator import singleton


@singleton
class ExceptionList(queue.Queue):
    def __init__(self):
        super().__init__()

    def print(self):
        while not self.empty():
            e = self.get()
            print(str(e))
