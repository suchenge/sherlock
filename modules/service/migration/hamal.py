import os.path

from modules.service.migration.overseer import Overseer
from modules.service.migration.task import TaskState, Task
from modules.service.migration.tracer import monitoring


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
    def __copy_file__(self, task: Task):
        try:
            source_path = task.source_path
            target_path = task.target_path

            with open(source_path, 'rb') as source_file, open(target_path, 'ab+') as target_file:
                target_size = os.path.getsize(target_path)
                try:
                    source_file.seek(target_size)
                    while True:
                        source_data = source_file.read(1024 * 1024)
                        if not source_data:
                            task.status = TaskState.DONE
                            break

                        target_file.write(source_data)
                        target_size += len(source_data)
                        task.target_size = target_size
                except Exception as error:
                    print('\r' + str(error))
                    task.status = TaskState.ERROR
                finally:
                    source_file.close()
                    target_file.close()

                    if task.status == TaskState.DONE:
                        self.__remove_txt__(task)

                    if task.status == TaskState.ERROR:
                        self.__remove_target_file__(task)
        except Exception as error:
            pass

    def __remove_txt__(self, task: Task):
        txt_path = task.target_path + '.txt'
        if os.path.exists(txt_path):
            os.remove(txt_path)

    def __remove_target_file__(self, task: Task):
        if os.path.exists(task.target_path):
            os.remove(task.target_path)

