import os
import time
import threading

from modules.migration.worker import Worker
from modules.migration.task import Task
from modules.migration.task import TaskState
from modules.migration.tracer import source_trace, target_trace


class Overseer(Worker):
    def __init__(self, directory):
        super(Overseer, self).__init__(directory)

        self.__tasks__ = [Task(element)
                          for element in self.__document__.findall('.//file')
                          if element.get('completeness') != '100.00%'
                          and (element.get('errors') is None
                               or int(element.get('errors')) < 3)]

        self.__task_index__ = -1
        self.__monitoring_task__ = None

    def start(self):
        super(Overseer, self).start()

    def stop(self):
        super(Overseer, self).stop()

    def get_task(self):
        if self.__monitoring_task__:
            self.__monitoring_task__.join()

        self.__task_index__ += 1
        if self.__task_index__ < len(self.__tasks__):
            task = self.__tasks__[self.__task_index__]
            if task.get_status() == TaskState.DONE \
                    or (os.path.exists(task.get_target_path()) and task.get_source_size() == os.stat(task.get_target_path()).st_size):
                task.set_status(TaskState.DONE)

                txt_path = task.get_target_path() + '.txt'
                if os.path.exists(txt_path):
                    os.remove(txt_path)
                return self.get_task()
            else:
                task.set_repetition(0)
                self.__monitoring_task__ = threading.Thread(target=self.__monitoring__, args=[task])
                self.__monitoring_task__.start()
                return task
        else:
            return None

    @source_trace
    def __monitoring__(self, task):
        while task and task.get_status() == TaskState.NEW:
            try:
                time.sleep(self.__sleep_time__)
                self.__monitoring_target__(task)
            except Exception as error:
                print(error)

    @target_trace
    def __monitoring_target__(self, task):
        if os.path.exists(task.get_target_path()):
            task.set_target_size(os.stat(task.get_target_path()).st_size)



