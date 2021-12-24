import time
import threading

from modules.migration.task import TaskState


def monitoring(fun):
    def wrapper(*args, **kwargs):
        obj = args[0]
        task = args[1]

        source_size = task.get_source_size()
        print('\r' + task.get_source_path() + ' | ' + str(source_size))

        copy_thread = threading.Thread(target=fun, args=[obj, task])
        copy_thread.setDaemon(True)
        copy_thread.start()

        target_size = task.get_target_size()

        while True:
            source_size_len = len(str(source_size))
            current_size = task.get_target_size()
            if current_size == target_size:
                task.set_repetition(task.get_repetition() + 1)
            else:
                target_size = current_size

            print(task.get_target_path()
                  + ' | ' + str(current_size).zfill(source_size_len)
                  + ' | ' + str('{:.2%}'.format(task.get_completeness() / 100)).zfill(7)
                  + ' | ' + str(task.get_repetition()).zfill(2)
                  + ' | ' + str(time.time()))

            if task.get_status() != TaskState.NEW:
                print('-----------------------------------------------------------')
                break

            time.sleep(5)
    return wrapper
