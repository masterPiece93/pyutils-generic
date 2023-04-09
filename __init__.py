from functools import wraps


def elf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def _exec(*options_args, **options_kwargs):
            # Yet to Extend *options_args, **options_kwargs
            return func(*args, **kwargs)

        return _exec

    return wrapper

