import time


class Task(object):
    def __init__(self, method, args=None, delay_seconds=0, in_queue_delay_seconds=0):
        self.__method__ = method
        self.__args__ = args
        self.__delay_seconds__ = delay_seconds
        self.__in_queue_delay_seconds__ = in_queue_delay_seconds

    @property
    def in_queue_delay_seconds(self):
        return self.__in_queue_delay_seconds__

    def run(self):
        if self.__delay_seconds__ > 0:
            time.sleep(self.__delay_seconds__)

        try:
            if self.__args__ is None:
                self.__method__()
            else:
                self.__method__(self.__args__)
        except Exception as error:
            pass
