import shutil

from modules.migration.overseer import Overseer
from modules.migration.task import TaskState


class Hamal(object):
    def __init__(self, directory):
        self.__overseer__ = Overseer(directory)
        self.__overseer__.start()

    def carry(self):
        task = self.__overseer__.get_task()
        if task is None:
            self.__overseer__.stop()
        else:
            try:
                source_path = task.get_source_path()
                target_path = task.get_target_path()

                shutil.copyfile(source_path, target_path)
                task.set_status(TaskState.DONE)
            except Exception as error:
                print('\r' + str(error))
                task.set_status(TaskState.ERROR)
            finally:
                self.carry()
