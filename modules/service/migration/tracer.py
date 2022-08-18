import time
import threading

from modules.service.migration.task import TaskState


def monitoring(fun):
    def wrapper(*args, **kwargs):
        obj = args[0]
        task = args[1]

        source_size = task.source_size
        print('\r' + task.source_path + ' | ' + str(source_size))

        copy_thread = threading.Thread(target=fun, args=[obj, task])
        copy_thread.setDaemon(True)
        copy_thread.start()

        target_size = task.target_size

        while True:
            source_size_len = len(str(source_size))
            current_size = task.target_size
            if current_size == target_size:
                task.repetition += 1
            else:
                target_size = current_size

            print(task.target_path
                  + ' | ' + str(current_size).zfill(source_size_len)
                  + ' | ' + str('{:.2%}'.format(task.completeness / 100)).zfill(7)
                  + ' | ' + str(task.repetition).zfill(2)
                  + ' | ' + str(time.time()))

            if task.status != TaskState.NEW:
                print('-----------------------------------------------------------')
                break

            time.sleep(5)
    return wrapper
