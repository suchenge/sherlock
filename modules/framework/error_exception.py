import sys
import traceback


class ErrorException(object):
    def __init__(self, error, sender=None):
        self.__error = error
        self.__exc_info__ = sys.exc_info()
        self.__traceback_info__ = traceback
        self.__sender_info__ = sender

    def __str__(self):
        exc_type, exc_value, exc_traceback = self.__exc_info__
        sender_info = ''
        if self.__sender_info__ is not None:
            sender_info = str(self.__sender_info__)

        return 'Exception:\nsender:%s\ninformation:%s\nmessage:%s\ntraceback\n\t%s\n\t%s\t%s\n' % (sender_info, '', exc_value, exc_traceback, self.__traceback_info__.print_exc(), self.__traceback_info__.format_exc())

