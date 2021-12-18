import os
import shutil
import time
import threading

from modules.migration.overseer import Overseer


class Hamal(object):
    def __init__(self, directory):
        self.__overseer__ = Overseer(directory)
        self.__overseer__.start()

    def carry(self):
        source_path, target_path = self.__overseer__.get_task()
        if source_path is None or target_path is None:
            self.__overseer__.stop()
        else:
            try:
                if os.path.exists(target_path):
                    source_size = os.stat(source_path).st_size
                    target_size = os.stat(target_path).st_size

                    if source_size != target_size:
                        self.__copyfile__(source_path, target_path)
                else:
                    self.__copyfile__(source_path, target_path)

                self.carry()
            except AttributeError:
                pass
            except Exception as error:
                print(error)
                self.carry()

    def __copyfile__(self, source_path, target_path):
        threading.Thread(target=shutil.copyfile, args=[source_path, target_path]).start()

        wait = threading.Thread(target=self.__thread_wait__)
        wait.start()
        wait.join()

    def __thread_wait__(self):
        while not self.__overseer__.stop_task:
            time.sleep(5)
            if self.__overseer__.stop_task:
                break
