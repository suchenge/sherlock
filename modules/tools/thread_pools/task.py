class Task(object):
    def __init__(self, method, args):
        self.__method__ = method
        self.__args__ = args

    def run(self):
        self.__method__(self.__args__)
