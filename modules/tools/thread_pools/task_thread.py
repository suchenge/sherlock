import threading


class TaskThread(threading.Thread):
    def __init__(self, thread_id, target):
        super().__init__()
        self.__id__ = thread_id
        self.__target__ = target

    def run(self) -> None:
        print("\n线程[%s]开始运行" % str(self.__id__))
        self.__target__()
        # super().run()
