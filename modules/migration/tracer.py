def source_trace(fun):
    def wrapper(*args, **kwargs):
        task = args[1]
        print('\r' + task.get_source_path() + ' | ' + str(task.get_source_size()))
        fun(*args)

    return wrapper


def target_trace(fun):
    def wrapper(*args, **kwargs):
        task = args[1]
        fun(*args)

        source_size = task.get_source_size()
        source_size_len = len(str(source_size))
        target_size = task.get_target_size()

        print(task.get_target_path()
              + ' | ' + str(target_size).zfill(source_size_len)
              + ' | ' + str('{:.2%}'.format(task.get_completeness() / 100))
              + ' | ' + str(task.get_repetition()))

    return wrapper
