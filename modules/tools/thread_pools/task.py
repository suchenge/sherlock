import time


class Task(object):
    def __init__(self, method, args=(), kwargs=None, delay_seconds=0, in_queue_delay_seconds=0):
        self.__method__ = method
        self.__args__ = args
        self.__kwargs__ = kwargs
        self.__delay_seconds__ = delay_seconds
        self.__in_queue_delay_seconds__ = in_queue_delay_seconds

    @property
    def in_queue_delay_seconds(self):
        return self.__in_queue_delay_seconds__

    @property
    def args(self):
        if self.__args__:
            return self.__args__
        return self.__kwargs__

    def run(self):
        if self.__delay_seconds__ > 0:
            time.sleep(self.__delay_seconds__)

        try:
            if self.__kwargs__:
                self.__method__(**self.__kwargs__)
            else:
                if self.__args__ is None or len(self.__args__) == 0:
                    self.__method__()
                elif self.__method__.__code__.co_argcount > 1:
                    self.__method__(*self.__args__)
                else:
                    self.__method__(self.__args__)
        except Exception as error:
            pass
