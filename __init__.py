from collections import namedtuple
from functools import wraps


def elf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def _exec(*options_args, **options_kwargs):
            # Yet to Extend *options_args, **options_kwargs
            return func(*args, **kwargs)

        return _exec

    return wrapper

class Colors:
    _HEADER = "\033[95m"
    _BLUE = "\033[94m"
    _CYAN = "\033[96m"
    _GREEN = "\033[92m"
    _WARNING = "\033[93m"
    _FAIL = "\033[91m"
    _ENDC = "\033[0m"
    _BOLD = "\033[1m"
    _UNDERLINE = "\033[4m"

    @classmethod
    def cprint(cls, *args, **kwargs):
        """Provides functions for various color printing."""
        colorfunc = namedtuple(
            "colorfunc",
            """
                header,
                blue,
                cyan,
                green,
                warning,
                fail,
                bold,
                underline
            """,
        )

        return colorfunc(
            lambda: print(cls._HEADER, *args, cls._ENDC, **kwargs),
            lambda: print(cls._BLUE, *args, cls._ENDC, **kwargs),
            lambda: print(cls._CYAN, *args, cls._ENDC, **kwargs),
            lambda: print(cls._GREEN, *args, cls._ENDC, **kwargs),
            lambda: print(cls._WARNING, *args, cls._ENDC, **kwargs),
            lambda: print(cls._FAIL, *args, cls._ENDC, **kwargs),
            lambda: print(cls._BOLD, *args, cls._ENDC, **kwargs),
            lambda: print(cls._UNDERLINE, *args, cls._ENDC, **kwargs),
        )
