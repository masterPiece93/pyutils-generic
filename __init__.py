from functools import wraps
try:
    # Python 2.x
    import __builtin__ as b
except ImportError:
    # Python 3.x
    import builtins as b


__all_builtin_types__: list = [t for t in b.__dict__.values() if isinstance(t, type)]


def elf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def _exec(*options_args, **options_kwargs):
            # Yet to Extend *options_args, **options_kwargs
            return func(*args, **kwargs)

        return _exec

    return wrapper

