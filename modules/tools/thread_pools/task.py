class Task(object):
    def __init__(self, method, args=None):
        self.__method__ = method
        self.__args__ = args

    def run(self):
        if self.__args__ is None:
            self.__method__()
        else:
            self.__method__(self.__args__)
