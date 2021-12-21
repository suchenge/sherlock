import os

from modules.migration.worker import Worker
from modules.migration.task import Task
from modules.migration.task import TaskState


class Overseer(Worker):
    def __init__(self, directory):
        super(Overseer, self).__init__(directory)

        self.__tasks__ = [Task(element)
                          for element in self.__document__.findall('.//file')
                          if element.get('completeness') != '100.00%'
                          and (element.get('errors') is None
                               or int(element.get('errors')) < 3)]

        self.__task_index__ = -1

    def start(self):
        super(Overseer, self).start()

    def stop(self):
        super(Overseer, self).stop()

    def get_task(self):
        self.__task_index__ += 1
        if self.__task_index__ < len(self.__tasks__):
            task = self.__tasks__[self.__task_index__]
            if task.get_status() == TaskState.DONE or (os.path.exists(task.get_target_path()) and task.get_source_size() == os.stat(task.get_target_path()).st_size):
                task.set_status(TaskState.DONE)
                return self.get_task()
            else:
                task.set_repetition(0)
                return task
        else:
            return None
