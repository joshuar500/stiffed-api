def optional_arg_decorator(func):
    def wrapper_decorator(*args, **kwargs):
        if len(args) == 1 and not kwargs and callable(args[0]):
            return func(args[0])
        else:
            def true_decorator(decorated):
                return func(decorated, *args, **kwargs)
            return true_decorator
    return wrapper_decorator