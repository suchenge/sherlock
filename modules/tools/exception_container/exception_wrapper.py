from modules.tools.exception_container.exception_list import ExceptionList


def exception_wrapper(record_exception_before_handler=None, record_exception_after_handler=None):
    def __func_wrapper__(func):
        def __args_wrapper__(*args, **kwargs):
            try:
                return func(*args, **kwargs)
                # if inspect.isclass(func) or inspect.isfunction(func):
                #     return func(*args, **kwargs)
                # if inspect.ismethod(func):
                #     func(*args, **kwargs)

            except Exception as error:
                if record_exception_before_handler is not None:
                    record_exception_before_handler(error, *args, **kwargs)

                ExceptionList().put(error)

                if record_exception_after_handler is not None:
                    record_exception_after_handler(error, *args, **kwargs)

        return __args_wrapper__

    return __func_wrapper__
