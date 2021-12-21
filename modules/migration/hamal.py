import os.path

from modules.migration.overseer import Overseer
from modules.migration.task import TaskState
from modules.migration.tracer import monitoring


class Hamal(object):
    def __init__(self, directory):
        self.__overseer__ = Overseer(directory)
        self.__overseer__.start()

    def carry(self):
        task = self.__overseer__.get_task()
        if task is None:
            self.__overseer__.stop()
        else:
            self.__copy_file__(task)
            self.carry()

    @monitoring
    def __copy_file__(self, task):
        source_path = task.get_source_path()
        target_path = task.get_target_path()

        with open(source_path, 'rb') as source_file, open(target_path, 'wb+') as target_file:
            target_size = os.path.getsize(target_path)
            try:
                while True:
                    source_data = source_file.read(1024 * 1024)
                    if not source_data:
                        task.set_status(TaskState.DONE)
                        break

                    target_file.write(source_data)
                    target_size += len(source_data)
                    task.set_target_size(target_size)
            except Exception as error:
                print('\r' + str(error))
                task.set_status(TaskState.ERROR)
            finally:
                source_file.close()
                target_file.close()

                if task.get_status() == TaskState.DONE:
                    self.__remove_txt__(task)

                if task.get_status() == TaskState.ERROR:
                    self.__remove_target_file(task)

    def __remove_txt__(self, task):
        txt_path = task.get_target_path() + '.txt'
        if os.path.exists(txt_path):
            os.remove(txt_path)

    def __remove_target_file(self, task):
        if os.path.exists(task.get_target_path()):
            os.remove(task.get_target_path())

