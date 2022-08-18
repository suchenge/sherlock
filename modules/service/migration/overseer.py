import os
from typing import Optional

from modules.service.migration.worker import Worker
from modules.service.migration.task import Task
from modules.service.migration.task import TaskState


class Overseer(Worker):
    def __init__(self, directory):
        super(Overseer, self).__init__(directory)

        self.__tasks__ = [Task(element)
                          for element in self.__document__.findall('.//file')
                          if element.get('completeness') != '100.00%'
                          and (element.get('errors') is None
                               or int(element.get('errors')) < 3)]

        self.__task_index__ = -1

    def get_task(self) -> Optional[Task]:
        self.__task_index__ += 1
        if self.__task_index__ < len(self.__tasks__):
            task = self.__tasks__[self.__task_index__]
            if task.status == TaskState.DONE or (
                    os.path.exists(task.target_path) and task.source_size == os.stat(task.target_path).st_size):
                task.status = TaskState.DONE
                return self.get_task()
            else:
                task.repetition = 0
                return task
        else:
            return None

    def __write_xml__(self):
        try:
            root = self.__document__.getroot()

            # 删除已经完成的file节点
            file_elements = root.findall('.//file[@completeness="100.00%"]')
            for element in file_elements:
                parent = root.find('.//path/file[@name="' + element.get('name') + '"]/...')
                parent.remove(element)

            if len(file_elements) > 0:
                # 删除所有file子节点都完成的path节点
                path_elements = [path for path in self.__document__.findall('.//path')
                                 if len([child for child in path.iter() if child is not path]) == 0]
                for element in path_elements:
                    parent = root.find('.//path[@name="' + element.get('name') + '"]/...')
                    parent.remove(element)
        except Exception as error:
            print(error)
        finally:
            super(Overseer, self).__write_xml__()
