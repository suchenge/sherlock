import os
import time
import threading

from modules.migration.worker import Worker


class Overseer(Worker):
    def __init__(self, directory):
        super(Overseer, self).__init__(directory)
        self.__task_index__ = -1
        self.__tasks__ = [element
                          for element in self.__document__.findall('.//file')
                          if element.get('completeness') != '100.00%'
                          and (element.get('errors') is None
                               or int(element.get('errors')) < 3)]

        self.__repetition_count__ = 10
        self.stop_task = False

    def start(self):
        super(Overseer, self).start()
        threading.Thread(target=self.__thread_update__).start()

    def stop(self):
        self.__task_index__ = -1
        self.stop_task = True

        super(Overseer, self).stop()

    def get_task(self):
        self.stop_task = False
        previous_task_index = self.__task_index__
        self.__task_index__ = -1
        time.sleep(self.__sleep_time__)

        self.__done_task__()

        source_path, target_path = None, None
        self.__task_index__ = previous_task_index + 1
        if self.__task_index__ < len(self.__tasks__):
            element = self.__tasks__[self.__task_index__]

            source_path = element[0].text
            target_path = element[1].text

            element.set('repetition', '0')

            print('\r' + source_path + ' | ' + element[0].get('size'))
        return source_path, target_path

    def __update_task__(self):
        element = None

        if self.__task_index__ > -1:
            try:
                element = self.__tasks__[self.__task_index__]
                source_node = element[0]
                source_path = source_node.text
                source_size = float(source_node.get('size'))

                target_node = element[1]
                target_path = target_node.text
                target_size = float(target_node.get('size'))

                if os.path.exists(target_path):
                    current_target_size = os.stat(target_path).st_size
                    completeness = '{:.2%}'.format(current_target_size / source_size)

                    target_node.set('size', str(current_target_size))
                    element.set('completeness', completeness)

                    repetition_count = 0
                    repetition = element.get('repetition')
                    if repetition:
                        repetition_count = int(repetition)

                    if current_target_size == target_size:
                        repetition_count += 1
                    else:
                        repetition_count = 0

                    element.set('repetition', str(repetition_count))

                    print(target_path
                          + ' | ' + completeness
                          + ' | ' + str(current_target_size)
                          + ' | ' + str(repetition_count))

                    if repetition_count > self.__repetition_count__:
                        self.stop_task = True

                    if current_target_size >= source_size:
                        self.stop_task = True

                        txt_path = target_path + '.txt'
                        if os.path.exists(txt_path):
                            os.remove(txt_path)
                            return None
            except Exception as error:
                print(error)

        return element

    def __done_task__(self):
        element = self.__update_task__()

        try:
            if element and self.__task_index__ > -1:
                errors_attribute = element.get('errors')
                if errors_attribute:
                    errors = int(errors_attribute) + 1
                else:
                    errors = 1

                element.set('errors', str(errors))
                element.set('repetition', '0')
        except Exception as error:
            print(error)

    def __thread_update__(self):
        while True:
            if self.__task_index__ > -1:
                self.__update_task__()
                time.sleep(self.__sleep_time__)
