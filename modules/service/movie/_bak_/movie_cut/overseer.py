import time
import threading

from os import system
from datetime import datetime
from modules.tools.common_methods.unity_tools import is_mac_os


def __mistiming_time__(start_time, end_time):
    seconds = (end_time - start_time).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


class Overseer(threading.Thread):
    def __init__(self, tasks):
        super().__init__()
        self.__tasks__ = tasks

    def __clear__(self):
        if is_mac_os() is False:
            system('cls')
        else:
            system('Clear')

    def run(self):
        while [task for task in self.__tasks__ if task['status'] != 'ending']:
            self.__clear__()
            print(self.__build_content__())
            time.sleep(1)

    def start(self):
        super().start()
        time.sleep(2)

    def join(self, timeout=None):
        super().join(timeout)
        time.sleep(5)

    def __build_content__(self):
        content = ''
        for task in self.__tasks__:
            output_name, output_path, start_time, end_time, length_time = task['timer_info']

            task_end_time = datetime.now()
            if task['status'] == 'ending':
                task_end_time = task['end_time']

            mistiming_time = __mistiming_time__(task['start_time'], task_end_time)

            content += '%s|%s|%s|%s|%s|%s|\n' % (output_name, start_time, end_time, length_time, task['status'], mistiming_time)

        return content

